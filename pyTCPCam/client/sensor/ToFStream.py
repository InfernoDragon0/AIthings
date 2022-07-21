import multiprocessing
import Jetson.GPIO as GPIO
import VL53L1X

from data.sensorInference import SensorInference


class ToFStream:

    # init and read one frame
    def __init__(self, tcp):
        self.tof = VL53L1X.VL53L1X(i2c_bus=1, i2c_address=0x29)
        self.distance = 0
        self.benchmark = 0
        self.tcp = tcp

    def startAsProcess(self):
        print("Sensor Stream Process started")
        self.tof.open()

        # self.sensorProcess = multiprocessing.Process(target=self.distance)
        self.sensorProcess = multiprocessing.Process(target=self.ToF, args=(self.tcp,))
        self.sensorProcess.start()
        return self

    # Setup
    def initBenchmark(self):
        initVal = self.tof.get_distance()
        cnt = 0
        total = initVal

        while True:
            self.distance = self.tof.get_distance()
            current = self.distance
            prev = self.distance
            if (current >= (initVal - (initVal * .03))) and (current <= (initVal + (initVal * .03))):
                total += current
                cnt += 1
            else:
                total -= prev
                cnt -= 1

            if cnt >= 5:
                self.benchmark = total / cnt
                break
            elif cnt <= -5:
                initVal = self.distance
                cnt = 0
                total = initVal

            self.tof.stop_ranging()

    # Get distance from ultrasonic sensor
    def ToF(self, tcp):
        while True:
            self.sensorInference = SensorInference("real ToF sensor")

            # 0 = Unchanged
            # 1 = Short Range
            # 2 = Medium Range
            # 3 = Long Range
            self.tof.start_ranging(3)  # Start ranging
            self.distance = self.tof.get_distance()
            print(str(self.distance) + 'mm')

            if (self.distance >= (self.benchmark - (self.benchmark * .03))) and (self.distance <= (self.benchmark + (self.benchmark * .03))):
                self.sensorInference.addData('0')
                print(f"ToF sensor state: 0")
            else:
                self.sensorInference.addData('1')
                print(f"ToF sensor state: 1")

            tcp.sendData(self.sensorInference)
            self.tof.stop_ranging()