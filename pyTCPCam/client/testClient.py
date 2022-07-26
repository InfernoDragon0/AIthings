#run main
import multiprocessing

import jsonpickle
from audio.audioStream import AudioStream
from audio.audioProcessor import AudioProcessor
from sensor.ultrasonicStream import UltrasonicStream
from sensor.vibrationStream import vibrationStream
from sensor.sensorStream import SensorStream
from video.videoTracker import VideoTracker
from data.configData import ConfigData
from clientTCP import ClientTCP
from video.videoEncoder import VideoEncoder
from video.videoProcessor import VideoProcessor
from video.videoStream import VideoStream

#config files
from pathlib import Path

if __name__ == '__main__':
    camQueue = multiprocessing.Queue(1) #only put the latest image in the queue
    encQueue = multiprocessing.Queue(1)
    resultQueue = multiprocessing.Queue(1)
    audQueue = multiprocessing.Queue(1)
    trackedQueue = multiprocessing.Queue(1)
    trackedResultQueue = multiprocessing.Queue(1)
    countQueue = multiprocessing.Queue(1)
    
    #config read
    config = ConfigData()

    configFile = Path("config.json")
    if configFile.exists():
        print("file exists")
        f = open(configFile, "r")
        config = jsonpickle.decode(f.read())
        
    else:
        f = open(configFile, "w+")
        print("creating new config file")
        newConfig = jsonpickle.encode(config, indent=4)
        f.write(newConfig)
    #config write

    imageModel = VideoProcessor(camQueue, encQueue, resultQueue, config.videoModel, config.videoInferenceType).startAsProcess()
    imageTracker = VideoTracker(encQueue, trackedQueue, trackedResultQueue, resultQueue, config.maxFrameLoss, config.targetFPS, countQueue).startAsProcess()
    # #start each video stream as a separate process
    videoStream0 = VideoStream(config.videoSource, config.targetFPS, camQueue, config.videoDebug).startAsProcess()
    tcp = ClientTCP(config.tcpName, config.tcpHost, config.tcpPort)
    # #audio process
    audioStream0 = AudioStream(config.audioBitRate, audQueue, config.audioSource, config.audioListenType, config.audioListenTime).startAsProcess()
    audioProcessor = AudioProcessor(config.audioModel, config.audioListenTime, audQueue, tcp, config.audioInferenceType).startAsProcess()

    # sensor process
    #sensorStream = SensorStream(tcp).startAsProcess()
    vibrationStream0 = vibrationStream(tcp).startAsProcess()
    ultrasonicStream = UltrasonicStream(tcp).startAsProcess()

    # #encoder and TCP
    videoEncoder0 = VideoEncoder(trackedQueue, trackedResultQueue, config.tcpSendTime, tcp, config.videoInferenceType, countQueue).start()
