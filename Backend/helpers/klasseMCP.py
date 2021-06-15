import time
import spidev


class SPI:
    def __init__(self, bus=0, device=0):
        # initialiseer een SpiDev-object
        self.spi = spidev.SpiDev()

        # open bus 0, device 0
        self.spi.open(bus, device)

        # stel de klokfrequentie in op 100kHz
        self.spi.max_speed_hz = 10 ** 5

    def read_channel(self, ch):
        # stel de commandobyte samen
        channel = ch << 4 | 128

        # maak een list met de 3 te versturen bytes,
        send_bytes = [0b00000001, channel, 0b00000000]

        # versturen en 3 bytes terugkrijgen
        receive_bytes = self.spi.xfer(send_bytes)

        # haal daar de meetwaarde (0-1024) uit en druk ze af
        result = (receive_bytes[1] & 3) << 8 | receive_bytes[2]
        return result

    def close_spi(self):
        self.spi.close()

    def read_air(self):
        return round(self.read_channel(0)/1023*100)

    def read_moist(self):
        return round(self.read_channel(1)/1023*100)

# spi = SPI()
# try:
#     while True:
#         print(spi.read_moist())
#         time.sleep(0.5)
# except KeyboardInterrupt as e:
#     print(e)
# finally:
#     spi.close_spi()