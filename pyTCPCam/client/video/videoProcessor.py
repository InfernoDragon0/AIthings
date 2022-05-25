from threading import Thread
from yolov5 import custom
from yolo_wrapper import Process
import simplejpeg

#unified to be able to change the sequence of these without any issues
class VideoProcessor():
    def __init__(self, stream):
model = Process(device=0, weights="./atasv3.pt")
        self.completed = False
        self.stream = stream
        self.processedFrame = self.stream.getFrame() #TODO apply the AI here one time if possible
        self.ready = False
    
    def start(self):
        Thread(target=self.process, args=()).start()
        return self

    #encode loop to encode the latest frame received
    def process(self):
        while True:
            if self.completed:
                return
            
            #decode the encoded image first to be inferred
            image = simplejpeg.decode_jpeg(self.encoder.encodedFrame , colorspace='BGR')
            #self.processedFrame is used to get the current frame
            #infer the image with the model to get the result
            result = model.inference_json_result(image)
            # print(result)

            #drawing the bounding boxes based on the result on the image
            image = model.draw_box_xyxy(image, result)
            self.setProcessedFrame(image)
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