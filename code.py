# Orchid greenhouse - sensor test
# Checks all 3 sensors every 3 seconds and prints what it finds.

import time
import board
from adafruit_bme280 import basic as adafruit_bme280
from adafruit_seesaw.seesaw import Seesaw
import adafruit_bh1750

i2c = board.STEMMA_I2C()   # the "talking line" for all sensors

air = None
soil = None
light = None

while True:
    print("------------------------------")

    # Who is connected? Ask the talking line.
    while not i2c.try_lock():
        pass
    found = i2c.scan()
    i2c.unlock()
    print("Devices found:", [hex(a) for a in found])

    # AIR sensor (BME280) - address 0x77
    try:
        if air is None:
            air = adafruit_bme280.Adafruit_BME280_I2C(i2c)
        print("AIR:   OK   temp =", round(air.temperature, 1), "C",
              "  humidity =", round(air.relative_humidity), "%")
    except Exception:
        air = None
        print("AIR:   not found")

    # SOIL sensor - address 0x36
    try:
        if soil is None:
            soil = Seesaw(i2c, addr=0x36)
        print("SOIL:  OK   moisture =", soil.moisture_read())
    except Exception:
        soil = None
        print("SOIL:  not found")

    # LIGHT sensor (BH1750) - address 0x23
    try:
        if light is None:
            light = adafruit_bh1750.BH1750(i2c)
        print("LIGHT: OK   light =", round(light.lux), "lux")
    except Exception:
        light = None
        print("LIGHT: not found")

    time.sleep(3)
