import simplejpeg
from threading import Thread
from data.imageInference import ImageInference
import time

#unified to be able to change the sequence of these without any issues
class VideoEncoder:
    def __init__(self, encQueue, resultQueue, fpsTarget, tcp, inferenceType, countQueue):
        self.tcp = tcp
        self.encQueue = encQueue
        self.resultQueue = resultQueue
        self.completed = False
        self.quality = 40
        self.ready = True
        self.timestamp = time.time()
        self.fps = 1/fpsTarget
        self.inferenceType = inferenceType
        self.countQueue = countQueue
    
    def start(self):
        Thread(target=self.encode, args=()).start()
        return self

    #encode loop to encode the latest frame received
    def encode(self):
        while True:
            if self.completed:
                return

            start = time.perf_counter()
            if not self.encQueue.empty() and not self.resultQueue.empty() and not self.countQueue.empty():
                self.frame = self.encQueue.get()
                self.results = self.resultQueue.get()
                self.encodedFrame = simplejpeg.encode_jpeg(self.frame, self.quality, colorspace='BGR')
                
                #and send the data over tcp, every x seconds
                if self.timestamp + self.fps < time.time():
                    self.timestamp = time.time()
                    self.imageInference = ImageInference(self.inferenceType)
                    self.imageInference.inferredData = self.results
                    self.imageInference.imageData = self.encodedFrame
                    self.imageInference.objectCount = self.countQueue.get()
                    self.tcp.sendData(self.imageInference)
                #print("video encoder is encoding & sending to server...")
            end = time.perf_counter()

            if (self.fps - (end - start) > 0):
                time.sleep(self.fps - (end - start))
            
            
    
    #end the thread
    def complete(self):
        self.completed = True