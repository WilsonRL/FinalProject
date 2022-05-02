################################################################################
# code.py
# Rebecca Wilson
# Last Modified April 14, 2022
#
# ABOUT
# This program runs on an Adafruit Feather (RP2040) equipped with an AirLift
# FeatherWing ESP32 WiFi CoProcessor. It is connected to a 12-channel capacitive
# touch sensor breakout (MPR121 - STEMMA QT), a STEMMA speaker and a button that
# downloads the mp3 files when pressed and connected to WiFi. 
#
# REQUIRED FILES
# (01) secrets.py -> contains sensitive information (your WiFi password and SSID)
# (02) boot.py -> allows download of files 
# (03) lib folder that contains:
#      - adafruit_bus_device    (folder with all files)
#      - adafruit_esp32spi      (folder with all files)
#      - adafruit_featherwing   (folder with all files)
#      - adafruit_io
#      - adafruit_mpr121.mpy
#      - adafruit_requests.mpy
#      - simpleio.mpy
#
# REFERENCES
# [1] https://learn.adafruit.com/adafruit-airlift-featherwing-esp32-wifi-co-processor-featherwing/internet-connect
# [2] https://likegeeks.com/downloading-files-using-python/
# [3] https://learn.adafruit.com/circuitpython-essentials/circuitpython-storage
# [4] https://learn.adafruit.com/cpu-temperature-logging-with-circuit-python?view=all
# [5] https://learn.adafruit.com/adafruit-mpr121-12-key-capacitive-touch-sensor-breakout-tutorial/python-circuitpython
# [6] https://learn.adafruit.com/circuitpython-essentials/circuitpython-mp3-audio
# [7] https://learn.adafruit.com/adafruit-io-basics-airlift/circuitpython
# [8] https://learn.adafruit.com/adafruit-io-basics-digital-input/arduino-wiring
# [9] https://learn.adafruit.com/multi-tasking-with-circuitpython/buttons
# [10] https://docs.circuitpython.org/projects/rgbled/en/stable/
# 
# NOTES
# [1] boot.py which is required to write files to the feather 
#     - you need to connect pin D5 to ground for file download and you need to 
#       disconnect that wire to copy files when connected to a computer
# [2] You will need to connect to WiFi download the twelve mp3 files and the 
#     words.txt file.
################################################################################

# basic libraries
import time
import board
import busio
# adafruit_requests usage with an esp32spi_socket
from digitalio import DigitalInOut, Direction, Pull
import adafruit_esp32spi.adafruit_esp32spi_socket as socket
from adafruit_esp32spi import adafruit_esp32spi
import adafruit_requests as requests
# capacitive touch sensor
import adafruit_mpr121
# adafruit io
from adafruit_io.adafruit_io import IO_HTTP, AdafruitIO_RequestError
# audio libraries
from audiomp3 import MP3Decoder
try:
    from audioio import AudioOut
except ImportError:
    try:
        from audiopwmio import PWMAudioOut as AudioOut
    except ImportError:
        pass  # not always supported by every board!

#CONSTANTS
NUMBER_OF_BUTTONS = 12

# import sensitive data from secrets file
try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

# pins if you have an AirLift Featherwing
esp32_cs = DigitalInOut(board.D13)
esp32_ready = DigitalInOut(board.D11)
esp32_reset = DigitalInOut(board.D12)

# create the serial peripheral interface bus (SPI) that lets the feather interact
# with the AirLift WiFi FeatherWing
spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)

# connect to WiFi via access point (AP) - try 4 times and then give up so board works without wifi
#print("Connecting to AP...")
while not esp.is_connected:
    try:
        esp.connect_AP(secrets["ssid"], secrets["password"])
    except RuntimeError as e:
        print("could not connect to AP, retrying: ", e)
        continue
print("Connected to", str(esp.ssid, "utf-8"), "\tRSSI:", esp.rssi)

# initialize a requests object with a socket and esp32spi interface
socket.set_interface(esp)
requests.set_socket(socket, esp)

# get relevant data from secrets file
aio_username = secrets["aio_username"]
aio_key = secrets["aio_key"]

# Initialize an Adafruit IO HTTP API object
io = IO_HTTP(aio_username, aio_key, requests)
try:
    #Get the 'aac-for-dogs' feed from Adafruit IO
    aac_feed = io.get_feed("aac-for-dogs")
except AdafruitIO_RequestError:
    #If no 'aac-for-dogs' feed exists, create one
    aac_feed = io.create_new_feed("aac-for-dogs")

# create list of mp3 files
mp3files = []
for i in range(NUMBER_OF_BUTTONS):
    mp3files.append("{}.mp3".format(i))

# create decoder to play audio (you have to specify a file in order to create the decoder)
mp3 = open(mp3files[0], "rb")
decoder = MP3Decoder(mp3)
audio = AudioOut(board.A0)

# pin set-up for button
button = DigitalInOut(board.D6)
button.direction = Direction.INPUT
button.pull = Pull.UP

# pins for capacitive touch MPR121
i2c = busio.I2C(board.SCL, board.SDA)
mpr121 = adafruit_mpr121.MPR121(i2c)

# create list of words associated with each button
words = []
myFile = open("words.txt", 'r')
for word in myFile:
    words.append(word)
myFile.close()
time.sleep(0.1)

# listens for contact with the capacitive touch sensor
while True:
    #if button is pressed
    if (not button.value):
        #get files from RPi server
        for i in range(NUMBER_OF_BUTTONS):
            # you will need to change this to your server address
            #response = requests.get("http://192.168.1.201:5000/uploads/{}.mp3".format(i))
            response = requests.get("http://192.168.1.181:8000/uploads/{}.mp3".format(i))
            myFile = open("/{}.mp3".format(i), 'wb')
            myFile.write(response.content)
            myFile.flush()
            response.close()

        # get text file of words
        #response = requests.get("http://192.168.1.201:5000/uploads/words.txt")
        response = requests.get("http://192.168.1.181:8000/uploads/words.txt")
        myFile = open("/words.txt", 'wb')
        myFile.write(response.content)
        myFile.flush()
        response.close()

        # create list of words associated with each button
        words = []
        myFile = open("words.txt", 'r')
        for word in myFile:
            words.append(word)
        myFile.close()
        time.sleep(0.1)

    # check to see if a button is pressed
    for i in range(NUMBER_OF_BUTTONS):
        # when a button is pressed
        if mpr121[i].value:
            # play associated mp3 file
            decoder.file = open(mp3files[i], "rb")
            audio.play(decoder)
            # send associated word to adafruit IO
            io.send_data(aac_feed["key"], words[i])
    time.sleep(0.1)
