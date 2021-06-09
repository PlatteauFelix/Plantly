import RPi.GPIO as GPIO
import time


class Speaker:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(19, GPIO.OUT)
        self.pwm = GPIO.PWM(19, 100)
        self.pwm.start(0)

    def playAlarm(self):
        self.pwm.ChangeDutyCycle(1)
        for i in range(500, 1200):
            self.pwm.ChangeFrequency(i)
            time.sleep(0.001)
            print(i)

    def playTone(self):
        self.pwm.ChangeDutyCycle(80)
        self.pwm.ChangeFrequency(800)
        time.sleep(0.25)
        self.pwm.ChangeDutyCycle(0)
        time.sleep(1)
        

    def quiet(self):
        self.pwm.ChangeDutyCycle(0)

    def stop(self):
        self.pwm.stop()


# speaker = Speaker()
# while True:
#     speaker.playTone()
