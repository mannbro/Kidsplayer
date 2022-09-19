# Music Player for Toddler using Raspberry Pi Pico and DFPlayer
This is a simple mp3 player with a screenless UI for Toddlers. It uses a Raspberry Pi Pico, a DFPlayer mp3-player module, some push buttons and leds.

In order to drive the DFPlayer MP3 player, it uses the drivers that are located here: https://github.com/mannbro/PicoDFPlayer

## YouTube Video
To learn more, check out the YouTube video I made about the player

[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/1--GBKYXRyY/0.jpg)](https://www.youtube.com/watch?v=1--GBKYXRyY)

## Circuit Diagram
![Circuit Diagram](https://github.com/mannbro/Kidsplayer/raw/main/circuit.png)

## Installation
Add the picodfplayer.py (from https://github.com/mannbro/PicoDFPlayer) and the kidsplayer.py to the root folder of your Pi Pico. To autostart, rename the. kidsplayer.py file to main.py before adding it to the Pi Pico.
