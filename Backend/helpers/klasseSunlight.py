from RPi import GPIO
import time
import seeed_si114x

class Sunlight:
    def __init__(self):
        self.sensor = seeed_si114x.grove_si114x()

    def read_values(self):
        return self.sensor.ReadVisible, self.sensor.ReadUV/100, self.sensor.ReadIR
    

# sunlight = Sunlight()
# try:
#     while True:
#         print(sunlight.read_values())
#         time.sleep(1)

# except KeyboardInterrupt as e:
#     print(e)
# finally:
#     GPIO.cleanup()
#     print("Script has stopped")