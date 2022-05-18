import simplejpeg
from threading import Thread

#TODO in addition, reduce the size of the jpeg before sending
class ClientEncoder:
    def __init__(self, stream):
        self.stream = stream
    
    def start(self):
        Thread(target=self.encode, args=()).start()
        return self

    def encode(self):
        while True:
            if self.completed:
                return

            frame = self.stream.getFrame()
            if (frame == None): continue #skip the frame if it is still being prepared
            self.encodedFrame = simplejpeg.encode_jpeg(frame, quality=40, colorspace='BGR') #40 has minimal difference to the eyes
    
    def getEncodedFrame(self):
        return self.encodedFrame
    
    def complete(self):
        self.completed = True