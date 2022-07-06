#Base class to be inherited for other inferences
class ConfigData():
    def __init__(self): #initialize base, this is for a single video source, single audio source  
        self.videoSource = "/dev/video0"
        self.videoModel = "./atasv3.pt"
        self.videoDebug = False
        self.targetFPS = 60
        self.videoInferenceType = "face"

        self.audioSource = 11
        self.audioModel = "yamnet.tflite"
        self.audioListenTime = 1
        self.audioListenType = "numpy_tf"
        self.audioBitRate = 16000
        self.audioInferenceType = "people"

        self.tcpHost = "127.0.0.1"
        self.tcpPort = 8100
        self.tcpName = "Integrated Audio/Video Client"
        self.tcpSendTime = 5
        
    
