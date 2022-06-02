from time import sleep
import cv2
from threading import Thread

class VideoStream:

    #init and read one frame
    def __init__(self, camera):
        self.stream = cv2.VideoCapture(camera)
        (self.available, self.frame) = self.stream.read()
        self.completed = False
    
    #run a thread to read all the frames continuously
    def start(self):
        print("Stream Thread started")
        Thread(target=self.readFrames, args=()).start()
        return self
    
    #Read loop for getting OpenCV images
    def readFrames(self):
        while True:
            #print("running while loop")
            if self.completed:
                return
            
            (self.available, self.frame) = self.stream.read()
            #if (self.available):
                #print("frame available")
            #else:
                #print("Not available")
            sleep(0.2)
            
    
    #get the latest frame
    def getFrame(self):
        return self.frame
        #return cv2.resize(self.frame, (1280, 720))
    
    #end the thread
    def complete(self):
        self.completed = True
        cv2.destroyAllWindows()

    def startDebug(self):
        Thread(target=self.showFrames, args=()).start()
        return self

    def showFrames(self):
        while True:
            if self.completed:
                return

            cv2.imshow('clientFrame', self.getFrame())
            cv2.waitKey(1)