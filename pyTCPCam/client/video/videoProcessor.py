from threading import Thread
from yolov5 import custom
from yolo_wrapper import Process
import cv2
import simplejpeg

model = Process(device=0, weights="./atasv3.pt")
#unified to be able to change the sequence of these without any issues
class VideoProcessor():
    def __init__(self, stream):
        self.completed = False
        self.stream = stream
        self.processedFrame = self.stream.getFrame()
        self.ready = False
    
    def start(self):
        Thread(target=self.process, args=()).start()
        return self

    #encode loop to encode the latest frame received
    def process(self):
        while True:
            if self.completed:
                return
            
            #self.processedFrame is used to get the current frame
            #infer the image with the model to get the result
            image = self.stream.getFrame()
            result = model.inference_json_result(image)

            #drawing the bounding boxes based on the result on the image
            image = model.draw_box_xyxy(image, result)
            self.setProcessedFrame(image)
            print("Processed")
            self.ready = True

    def asInferenceObject(self): #can remove if not needed
        return {"x": 123, "y": 234, "confidence": 1, "inferred": "Person"}

    #unified to reduce changes
    def getFrame(self):
        return self.processedFrame

    def setProcessedFrame(self, img):
        self.processedFrame = img

    #end the thread
    def complete(self):
        self.completed = True

        #run a thread to show frames continuously
    def startDebug(self):
        Thread(target=self.showFrames, args=()).start()
        return self

    def showFrames(self):
        while True:
            if self.completed:
                return

            cv2.imshow('clientFrame', self.getFrame())
            cv2.waitKey(1)