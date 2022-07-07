import multiprocessing
import RPi.GPIO as GPIO
import time


class sensorStream:

    # init and read one frame
    def __init__(self):
        self.GPIO_TRIGGER = 23
        self.GPIO_ECHO = 24

    def startAsProcess(self):
        print("Sensor Stream Process started")
        self.gpioSetup()

        self.sensorProcess = multiprocessing.Process(target=self.distance)
        self.sensorProcess.start()
        return self

    def gpioSetup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.GPIO_TRIGGER, GPIO.OUT)
        GPIO.setup(self.GPIO_ECHO, GPIO.IN)

    # Get distance from ultrasonic sensor
    def distance(self):
        while True:
            GPIO.output(self.GPIO_TRIGGER, True)
            time.sleep(0.0001)
            GPIO.output(self.GPIO_TRIGGER, False)

            while not GPIO.input(self.GPIO_ECHO):
                pass

            StartTime = time.time()

            while GPIO.input(self.GPIO_ECHO):
                pass

            StopTime = time.time()

            TimeElapsed = StopTime - StartTime
            distance = (TimeElapsed * 0.034) / 2
            time.sleep(0.3)
