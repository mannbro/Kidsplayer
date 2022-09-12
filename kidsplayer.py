from machine import UART, Pin
from utime import sleep_ms, sleep
from picodfplayer import DFPlayer

#Constants
UART_INSTANCE=0
TX_PIN = 16
RX_PIN=17
BUSY_PIN=22

WAIT_FOR_PLAYER_INIT=1000
WAIT_AFTER_BUTTON=500
WAIT_IN_MAIN_LOOP=50

DEFAULT_VOLUME=18

#Globals
paused=True

#Pins for Language LED:s
folders=[
    {'name': 'SE', 'led': Pin(21, Pin.OUT), 'filecount': 60},
    {'name': 'RU', 'led': Pin(20, Pin.OUT), 'filecount': 38},
    {'name': 'UA', 'led': Pin(19, Pin.OUT), 'filecount': 101},
    {'name': 'NL', 'led': Pin(18, Pin.OUT), 'filecount': 99}]




#Control Button Pins
btnPrevTrack=Pin(2, Pin.IN, Pin.PULL_UP)
btnPlayPause=Pin(3, Pin.IN, Pin.PULL_UP)
btnNextTrack=Pin(4, Pin.IN, Pin.PULL_UP)
btnNextFolder=Pin(5, Pin.IN, Pin.PULL_UP)

#DFPlayer
player=DFPlayer(UART_INSTANCE, TX_PIN, RX_PIN, BUSY_PIN)

def saveState():
    global state

    configFile=open('state','w')
    configFile.write(repr(state))
    configFile.close()

def loadState():
    global state

    try:
        configFile=open('state','r')
        state=eval(configFile.read())
        configFile.close()
    except:
        state={
            'currentFolder': 0,
            'currentTracks': [1,1,1,1]
        }

def getCurrentFolder():
    global state
    return state['currentFolder']
    
def setCurrentFolder(currentFolder):
    global state
    state['currentFolder']=currentFolder
    saveState()
    
def getCurrentTrack():
    global state
    return state['currentTracks'][state['currentFolder']]

def setCurrentTrack(currentTrack):
    global state
    state['currentTracks'][state['currentFolder']]=currentTrack
    saveState()

#Display selected language LED
def displayFolder():
    for idx, folder in enumerate(folders):
        if(idx==getCurrentFolder()):
            folder['led'].value(1)
        else:
            folder['led'].value(0)


#Select Next Folder
def nextFolder():
    currentFolder=getCurrentFolder()+1

    if(currentFolder==len(folders)):
        currentFolder=0

    setCurrentFolder(currentFolder)
    
    folder=folders[currentFolder]
    currentTrack=getCurrentTrack()

    displayFolder()
    playSelected()

#Next and previous tracks
def nextTrack():

    currentFolder=getCurrentFolder()
    currentTrack=getCurrentTrack()

    folder=folders[currentFolder]
    if currentTrack>=folder['filecount']:
        currentTrack=1
    else:
        currentTrack+=1
    
    setCurrentTrack(currentTrack)

    player.resume()
    playSelected()

def prevTrack():
    currentFolder=getCurrentFolder()
    currentTrack=getCurrentTrack()
    
    folder=folders[currentFolder]
    if currentTrack==1:
        currentTrack=folder['filecount']
    else:
        currentTrack-=1
    
    setCurrentTrack(currentTrack)
    
    player.resume()
    playSelected()

def playPause():
    global paused
    
    if paused:
        paused=False
        player.resume()
    else:
        paused=True
        player.pause()
        
def playSelected():
    global paused

    #1 is added because arrays are zero based, but folders start on 1
    currentFolder=getCurrentFolder()+1
    currentTrack=getCurrentTrack()
    
    paused=False
    print(currentFolder, currentTrack)
    player.playTrack(currentFolder, currentTrack)

def init():
    loadState()
    #Wait to ensure that DFPlayer is initiated
    displayFolder()
    sleep_ms(WAIT_FOR_PLAYER_INIT)
    player.setVolume(DEFAULT_VOLUME)
    playSelected()

    mainLoop()

    

def mainLoop():
    while True:
        if not btnNextFolder.value():
            nextFolder()
            sleep_ms(WAIT_AFTER_BUTTON)
        elif not btnPrevTrack.value():
            prevTrack()
            sleep_ms(WAIT_AFTER_BUTTON)
        elif not btnNextTrack.value():
            nextTrack()
            sleep_ms(WAIT_AFTER_BUTTON)
        elif not btnPlayPause.value():
            playPause()
            sleep_ms(WAIT_AFTER_BUTTON)
        elif player.playerBusy.value() and not paused:
            nextTrack()           
            sleep_ms(WAIT_AFTER_BUTTON)

        sleep_ms(WAIT_IN_MAIN_LOOP)

init()
