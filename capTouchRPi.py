# References
# [1] https://learn.adafruit.com/adafruit-mpr121-12-key-capacitive-touch-sensor-breakout-tutorial

#import libraries
import time
import board
import busio
import adafruit_mpr121

# Connect 
# Pi 3V3 to sensor VIN
# Pi GND to sensor GND
# Pi SCL to sensor SCL
# Pi SDA to sensor SDA
# one wire to each of the 12 sensor pins (0-11)
i2c = busio.I2C(board.SCL, board.SDA)
mpr121 = adafruit_mpr121.MPR121(i2c)

while True:
    for i in range(12):
        if mpr121[i].value:
            print("Pin {} touched".format(i))                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             
