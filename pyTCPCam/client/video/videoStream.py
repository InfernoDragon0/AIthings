import multiprocessing
import time
import cv2
from threading import Thread

class VideoStream:

    #init and read one frame
    def __init__(self, camera, fpsTarget, camQueue):
        self.camera = camera
        self.completed = False
        self.fps = 1/fpsTarget
    
    def startAsProcess(self):
        print("Stream Process started")
        self.camProcess = multiprocessing.Process(target=self.readFrames, args=(self.fps, self.camera, True))
        self.camProcess.start()
        return self
    
    #Read loop for getting OpenCV images
    def readFrames(self, fps, camera, debug):
        self.stream = cv2.VideoCapture(camera)
        self.stream.set(cv2.CAP_PROP_BUFFERSIZE, 2) #lower the buffer size
        while True:
            if self.completed:
                return
            
            (self.available, self.frame) = self.stream.read()
            if debug:
                cv2.imshow('clientFrame', self.frame)
                cv2.waitKey(1)
            time.sleep(fps)
    
    #get the latest frame
    def getFrame(self):
        return self.frame
        #return cv2.resize(self.frame, (1280, 720))
    
    #end the thread
    def complete(self):
        self.completed = True
        cv2.destroyAllWindows()