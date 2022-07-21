import multiprocessing
import Jetson.GPIO as GPIO
import time

from data.sensorInference import SensorInference


class UltrasonicStream:

    # init and read one frame
    def __init__(self, tcp):
        self.GPIO_TRIGGER = 11
        self.GPIO_ECHO = 8
        self.distance = 0.0
        self.benchmark = 0.0
        self.tcp = tcp

    def startAsProcess(self):
        print("Sensor Stream Process started")
        self.gpioSetup()
        self.initBenchmark()

        # self.sensorProcess = multiprocessing.Process(target=self.distance)
        self.sensorProcess = multiprocessing.Process(target=self.Distance, args=(self.tcp,))
        self.sensorProcess.start()
        return self

    def gpioSetup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.GPIO_TRIGGER, GPIO.OUT)
        GPIO.setup(self.GPIO_ECHO, GPIO.IN)

    def initBenchmark(self):
        self.getDistance()
        initVal = self.distance
        cnt = 0
        total = initVal
        print("before while")
        time.sleep(0.0001)
        while True:
            print("after while")
            print(cnt)
            self.getDistance()
            current = self.distance
            prev = self.distance
            print("after get distance")
            if (current >= (initVal - (initVal * .05))) and (current <= (initVal + (initVal * .05))):
                total += current
                cnt += 1
                print("+1")
            else:
                total -= prev
                cnt -= 1
                print("-1")

            if cnt >= 5:
                self.benchmark = total / cnt
                print("after>=5")
                break
            elif cnt <= -5:
                initVal = self.distance
                cnt = 0
                total = initVal
                print("reset")

            time.sleep(0.0001)

    #  Ultrasonic sensor main loop
    def Distance(self, tcp):
        print("Start sensor")
        while True:
            self.sensorInference = SensorInference("real ultrasonic sensor")

            self.getDistance()
            if (self.distance >= (self.benchmark - (self.benchmark * .05))) and (
                    self.distance <= (self.benchmark + (self.benchmark * .05))):
                self.sensorInference.addData('0')
                print(f"sensor time: 0")
            else:
                self.sensorInference.addData('1')
                print(f"sensor time: 1")

            tcp.sendData(self.sensorInference)
            print(f"sensor distance: {self.distance}")
            time.sleep(0.3)

    # Get distance from ultrasonic sensor
    def getDistance(self):
        GPIO.output(self.GPIO_TRIGGER, True)
        time.sleep(0.00001)
        GPIO.output(self.GPIO_TRIGGER, False)

        while not GPIO.input(self.GPIO_ECHO):
            pass

        StartTime = time.time()

        while GPIO.input(self.GPIO_ECHO):
            pass

        StopTime = time.time()

        TimeElapsed = StopTime - StartTime
        self.distance = (TimeElapsed * 34300) / 2
