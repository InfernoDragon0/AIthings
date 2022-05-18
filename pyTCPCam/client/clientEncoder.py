import simplejpeg
from threading import Thread

#TODO in addition, reduce the size of the jpeg before sending
class ClientEncoder:
    def __init__(self, stream):
        self.stream = stream
        self.completed = False
        self.quality = 40
        self.encodedFrame = simplejpeg.encode_jpeg(self.stream.getFrame(), self.quality, colorspace='BGR') #encode the first frame
    
    def start(self):
        Thread(target=self.encode, args=()).start()
        return self

    #encode loop to encode the latest frame received
    def encode(self):
        while True:
            if self.completed:
                return

            self.encodedFrame = simplejpeg.encode_jpeg(self.stream.getFrame(), self.quality, colorspace='BGR')
    
    #get the latest encoded frame
    def getEncodedFrame(self):
        return self.encodedFrame
    
    #end the thread
    def complete(self):
        self.completed = True