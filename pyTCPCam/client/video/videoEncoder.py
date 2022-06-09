import jsonpickle
import simplejpeg
from threading import Thread
from data.imageInference import ImageInference
import time

#unified to be able to change the sequence of these without any issues
class VideoEncoder:
    def __init__(self, stream, tcp):
        self.tcp = tcp
        self.stream = stream
        self.completed = False
        self.quality = 40
        self.encodedFrame = simplejpeg.encode_jpeg(self.stream.getFrame(), self.quality, colorspace='BGR') #encode the first frame
        self.ready = True
        self.imageInference = ImageInference()
        self.timestamp = time.time()
        self.tcpTime = 1
    
    def start(self):
        Thread(target=self.encode, args=()).start()
        return self

    #encode loop to encode the latest frame received
    def encode(self):
        while True:
            time.sleep(0.2)
            if self.completed:
                return

            self.encodedFrame = simplejpeg.encode_jpeg(self.stream.getFrame(), self.quality, colorspace='BGR')
            
            #and send the data over tcp, every x seconds [TODO to send only when alert or something]
            if self.timestamp + self.tcpTime < time.time():
                self.timestamp = time.time()
                self.imageInference = ImageInference()
                self.imageInference.inferredData = self.stream.result
                self.imageInference.setImageData(self.encodedFrame)
                self.tcp.addData(self.imageInference)
                self.tcp.start()
                #print(jsonpickle.encode(self.imageInference))
    
    #unified to reduce changes
    def getFrame(self):
        return self.encodedFrame
    
    #end the thread
    def complete(self):
        self.completed = True