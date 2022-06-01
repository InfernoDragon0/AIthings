import cv2
from threading import Thread

class VideoStream:

    #init and read one frame
    def __init__(self, camera):
        self.stream = cv2.VideoCapture(camera, cv2.CAP_V4L2)
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
        #return cv2.resize(self.frame, (1280, 720))
    
    #end the thread
    def complete(self):
        self.completed = True
        cv2.destroyAllWindows()