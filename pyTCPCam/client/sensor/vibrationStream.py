import multiprocessing
import Jetson.GPIO as GPIO
import time

from data.sensorInference import SensorInference


class vibrationStream:

    # init and read one frame
    def __init__(self, tcp):
        self.GPIO_TRIGGER = 26

    def startAsProcess(self):
        print("Sensor Stream Process started")
        self.gpioSetup()

        # self.sensorProcess = multiprocessing.Process(target=self.distance)
        self.sensorProcess = multiprocessing.Process(target=self.Vibration, args=(self.tcp,))
        self.sensorProcess.start()
        return self

    def gpioSetup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.GPIO_TRIGGER, GPIO.IN)

    #  Ultrasonic sensor main loop
    def Vibration(self, tcp):
        print("Start sensor")
        while True:
            self.sensorInference = SensorInference("real vibration sensor")

            if GPIO.input(self.GPIO_TRIGGER):
                self.sensorInference.addData('1')
                print(f"sensor time: 1")
            else:
                self.sensorInference.addData('0')
                print(f"sensor time: 0")

            tcp.sendData(self.sensorInference)
            time.sleep(0.3)
