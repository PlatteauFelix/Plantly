from RPi import GPIO
import seeed_dht

class TempHumi:
    def __init__(self):
        # for DHT11 on pin 12
        self.sensor = seeed_dht.DHT('11', 12)

    def read_values(self):
        return self.sensor.read()


# temphumi = TempHumi()
# try:
#     while True:
#         print(temphumi.read_values())

# except KeyboardInterrupt as e:
#     print(e)
# finally:
#     GPIO.cleanup()
#     print("Script has stopped")