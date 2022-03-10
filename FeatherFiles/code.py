#REFERENCES
# [1] https://learn.adafruit.com/adafruit-airlift-featherwing-esp32-wifi-co-processor-featherwing/internet-connect
# [2] https://likegeeks.com/downloading-files-using-python/
# [3] https://learn.adafruit.com/circuitpython-essentials/circuitpython-storage
# [4] https://learn.adafruit.com/cpu-temperature-logging-with-circuit-python?view=all
# [5] https://learn.adafruit.com/adafruit-mpr121-12-key-capacitive-touch-sensor-breakout-tutorial/python-circuitpython
# [6] https://learn.adafruit.com/circuitpython-essentials/circuitpython-mp3-audio
# [7] https://learn.adafruit.com/adafruit-io-basics-airlift/circuitpython

# NOTES
# use reference 4 to create boot.py which is needed to write files to the feather

# basic libraries
import time
import board
import busio
# adafruit_requests usage with an esp32spi_socket
from digitalio import DigitalInOut
import adafruit_esp32spi.adafruit_esp32spi_socket as socket
from adafruit_esp32spi import adafruit_esp32spi
import adafruit_requests as requests
# capacitive touch sensor
import adafruit_mpr121
# audio ;ibraries
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

# pins for capacitive touch MPR121
i2c = busio.I2C(board.SCL, board.SDA)
mpr121 = adafruit_mpr121.MPR121(i2c)

# NOT SURE WHAT THIS DOES
spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)

# NOT SURE EXACTLY WHAT THIS DOES
print("Connecting to AP...")
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

# list of mp3 files
mp3files = []
for i in range(NUMBER_OF_BUTTONS):
    mp3files.append("{}.mp3".format(i))

# get files from RPi server
for i in range(NUMBER_OF_BUTTONS):
    # you will need to change this to your server address
    response = requests.get("http://192.168.1.201:5000/uploads/{}.mp3".format(i))
    myFile = open("/{}.mp3".format(i), 'wb')
    myFile.write(response.content)
    myFile.flush()
    response.close()
 
# NOT SURE WHAT THIS DOES
mp3 = open(mp3files[0], "rb")
decoder = MP3Decoder(mp3)
audio = AudioOut(board.A0)

# listens for contact with the capacitive touch sensor    
while True:
    for i in range(NUMBER_OF_BUTTONS):
        if mpr121[i].value:
            print("{}".format(i))
            decoder.file = open(mp3files[i], "rb")
            audio.play(decoder)
    time.sleep(0.5)
