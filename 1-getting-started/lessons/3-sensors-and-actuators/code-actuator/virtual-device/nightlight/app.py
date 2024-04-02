import time
from counterfit_connection import CounterFitConnection
from counterfit_shims_grove.grove_light_sensor_v1_2 import GroveLightSensor
from counterfit_shims_grove.grove_led import GroveLed

CounterFitConnection.init('127.0.0.1', 5000)

light_sensor = GroveLightSensor(0)
led = GroveLed(5)

while True:
    light = light_sensor.light
    print('Light level:', light)

    if light < 300:
        led.on()
        print("Led on")
    else:
        led.off()
        print("Led off")
    time.sleep(1)