import multiprocessing
import time
import cv2
from threading import Thread

class VideoStream:

    #init and read one frame
    def __init__(self, camera, fpsTarget, camQueue, debug):
        self.camera = camera
        self.completed = False
        self.fps = 1/fpsTarget
        self.camQueue = camQueue
        self.debug = debug
    
    def startAsProcess(self):
        print("Stream Process started")
        self.camProcess = multiprocessing.Process(target=self.readFrames, args=(self.fps, self.camera, self.debug, self.camQueue))
        self.camProcess.start()
        return self
    
    #Read loop for getting OpenCV images
    def readFrames(self, fps, camera, debug, camQueue):
        self.stream = cv2.VideoCapture(camera)
        self.stream.set(cv2.CAP_PROP_BUFFERSIZE, 2) #lower the buffer size
        while True:
            if self.completed:
                return
            
            start = time.perf_counter()
            (self.available, self.frame) = self.stream.read()
            if self.available:
                if camQueue.empty():
                    camQueue.put(self.frame) #only put into the queue if the previous frame is already consumed

                if debug:
                    cv2.imshow('clientFrame', self.frame)
                    cv2.resizeWindow("clientFrame", 960, 1080)
                    cv2.waitKey(1)
            end = time.perf_counter()
            if (fps - (end - start) > 0):
                time.sleep(fps - (end - start))
    
    #get the latest frame
    def getFrame(self):
        return self.frame
        #return cv2.resize(self.frame, (1280, 720))
    
    #end the thread
    def complete(self):
        self.completed = True
        cv2.destroyAllWindows()