import cv2
from threading import Thread

class ClientStream:

    #init and read one frame
    def __init__(self, camera):
        self.stream = cv2.VideoCapture(camera)
        (self.available, self.frame) = self.stream.read()
        self.completed = False
    
    #run a thread to read all the frames continuously
    def start(self):
        Thread(target=self.readFrames, args=()).start()
        return self
    
    #Read loop for getting OpenCV images
    def readFrames(self):
        while True:
            if self.completed:
                return
            
            (self.available, self.frame) = self.stream.read()
    
    #get the latest frame
    def getFrame(self):
        return self.frame
    
    #end the thread
    def complete(self):
        self.completed = True