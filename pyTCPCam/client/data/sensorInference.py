from data.baseInference import BaseInference


class SensorInference(BaseInference):
    def __init__(self, inferenceType):
        super().__init__()
        self.inferenceType = inferenceType #sensor name here, e.g. ultrasonic sensor, etc
        self.packetType = "Sensor"