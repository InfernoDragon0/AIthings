
from data.baseInference import BaseInference


class AudioInference(BaseInference):
    def __init__(self, inferenceType):
        super().__init__()
        self.inferenceType = inferenceType
        self.packetType = "Audio"
        self.audioData = None

    def addInferenceData(self, name, value):
        dict = {"name": name, "value": value}
        self.addData(dict)
    
    def setAudioData(self, audio): #if need to send audio over to server
        self.audioData = audio
