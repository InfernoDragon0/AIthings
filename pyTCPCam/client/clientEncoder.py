import time
import jsonpickle
import simplejpeg
from threading import Thread

from data.imageInference import ImageInference

#TODO in addition, reduce the size of the jpeg before sending
#TODO ClientEncoder to tell ClientTCP to send when ready
class ClientEncoder:
    def __init__(self, stream):
        self.stream = stream
        self.completed = False
        self.quality = 40
        self.encodedFrame = simplejpeg.encode_jpeg(self.stream.getFrame(), self.quality, colorspace='BGR') #encode the first frame
        self.ready = True
        self.imageInference = ImageInference(time.time())
    
    def start(self):
        Thread(target=self.encode, args=()).start()
        return self

    #encode loop to encode the latest frame received
    def encode(self):
        while True:
            if self.completed:
                return

            self.encodedFrame = simplejpeg.encode_jpeg(self.stream.getFrame(), self.quality, colorspace='BGR')
            self.imageInference = ImageInference(time.time())
            self.imageInference.setImageData(self.encodedFrame)
            self.imageInference.addData({"temporray": "encoder"})
            self.ready = True
            #print(jsonpickle.encode(self.imageInference))
    
    #get the latest encoded frame
    def getEncodedFrame(self):
        return self.encodedFrame
    
    #end the thread
    def complete(self):
        self.completed = True