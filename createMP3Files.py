# REFERENCES
# [1] https://www.geeksforgeeks.org/convert-text-speech-python/
# [2] https://chrisrosser.net/posts/2020/04/06/using-sox-on-macos/

# NOTES
# In order for this file to play the audio files, you need to have the
# speaker connected to the RPi (USB and audio jack)
# You may need to install the following libraries:
# pip install gTTS
# on mac (assuming you use  homebrew):
# brew install sox 
# on RPi:
# sudo apt-get install sox
# sudo apt-get install libsox-fmt-mp3

# Import libraries
from gtts import gTTS
import os

# This is the text to convert to audio
text = ["outside", "play", "swimming", "chew", "dinner",
        "treat", "walk", "help", "come", "now", "later",
        "done"]

# Language in which you want to convert
language = 'en'

# create and save the mp3 files
for i in range(len(text)):
    soundFile = gTTS(text = text[i], lang = language, slow = False)
    soundFile.save("{}.mp3".format(text[i]))

# Playing the file
for i in range(len(text)):
    os.system("play {}.mp3".format(text[i]))
