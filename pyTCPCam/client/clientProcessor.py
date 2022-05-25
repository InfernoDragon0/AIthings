from threading import Thread
from yolov5 import custom
from yolo_wrapper import Process
import simplejpeg

#TODO AI stuff in another thread, before the ClientEncoder. AI to tell ClientEncoder to encode (probably with a variable) when ready

#Setting up the model to be used for inferencing
model = Process(device=0, weights="./atasv3.pt")

class ClientProcessor():
    def __init__(self, encoder):
        self.completed = False
        self.encoder = encoder
        # self.processedFrame = self.encoder.encodedFrame #TODO apply the AI here one time if possible
        self.processedFrame = simplejpeg.decode_jpeg(self.encoder.encodedFrame) # decode the frame on receive
        self.ready = False
        pass
    
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

    #get the latest inferenced frame
    def getProcessedFrame(self):
        return self.processedFrame

    def setProcessedFrame(self, img):
        self.processedFrame = img

    #end the thread
    def complete(self):
        self.completed = True