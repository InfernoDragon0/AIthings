import time
import cv2
from threading import Thread

class VideoStream:

    #init and read one frame
    def __init__(self, camera, fpsTarget):
        self.stream = cv2.VideoCapture(camera)
        self.stream.set(cv2.CAP_PROP_BUFFERSIZE, 2) #lower the buffer size
        (self.available, self.frame) = self.stream.read()
        self.completed = False
        self.fps = 1/fpsTarget
    
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
            time.sleep(self.fps)
    
    #get the latest frame
    def getFrame(self):
        return self.frame
        #return cv2.resize(self.frame, (1280, 720))
    
    #end the thread
    def complete(self):
        self.completed = True
        cv2.destroyAllWindows()