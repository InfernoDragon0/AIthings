import jsonpickle
import simplejpeg
from threading import Thread
from data.imageInference import ImageInference

#unified to be able to change the sequence of these without any issues
class VideoEncoder:
    def __init__(self, stream):
        self.stream = stream
        self.completed = False
        self.quality = 40
        self.encodedFrame = simplejpeg.encode_jpeg(self.stream.getFrame(), self.quality, colorspace='BGR') #encode the first frame
        self.ready = True
        self.imageInference = ImageInference()
    
    def start(self):
        Thread(target=self.encode, args=()).start()
        return self

    #encode loop to encode the latest frame received
    def encode(self):
        while True:
            if self.completed:
                return

            if (not self.stream.ready):
                continue

            self.encodedFrame = simplejpeg.encode_jpeg(self.stream.getFrame(), self.quality, colorspace='BGR')
            #move to tcp side
            self.imageInference = ImageInference()
            self.imageInference.setImageData(self.encodedFrame)
            self.imageInference.addData({"temporray": "encoder"})
            self.stream.ready = False
            self.ready = True
            #print(jsonpickle.encode(self.imageInference))
    
    #unified to reduce changes
    def getFrame(self):
        return self.encodedFrame
    
    #end the thread
    def complete(self):
        self.completed = True