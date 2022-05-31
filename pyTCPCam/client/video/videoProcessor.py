from threading import Thread
from typing import final
from yolov5 import custom
from yolo_wrapper import Process
import cv2
import simplejpeg

#unified to be able to change the sequence of these without any issues
class VideoProcessor():
    def __init__(self, stream):
        self.model = Process(device=0, weights="./atasv3.pt")
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
            result = self.model.inference_json_result(image)

            if(len(result) > 1): #no need to bother with just 1 item in array
                result = self.nms(result)
            print(result)

            #drawing the bounding boxes based on the result on the image
            image = self.model.draw_box_xyxy(image, result)
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
    
    #filters the result to remove intersecting boxes
    def nms(self, result):
        # dictionary array to put those that are not intersecting
        final_dict_array = []

        # FILTERING LOWER SCORES OUT (below 0.5)
        dict_array = [dict for dict in result if dict['score'] > 0.5] 
        
        while(len(dict_array) > 0):
            # FILTERING THE MAX SCORE 
            maxscore_box = max(dict_array, key=lambda x:x['score']) #returns highest score dict
            final_dict_array.append(maxscore_box) #add highest score into final array 
            x0, y0, x1, y1 = maxscore_box['box'] #box to be compared against later
            # getting area of maxscore box
            msb_area = float((x1 - x0) * (y1 - y0))

            # dictionary array with the highest now removed (to not compare with itself)
            dict_array = [dict for dict in dict_array if dict['score'] < maxscore_box['score']]

            for dict in list(dict_array):
                X0, Y0, X1, Y1 = dict['box']
                width = self.calculateIntersection(X0, X1, x0, x1)
                height = self.calculateIntersection(Y0, Y1, y0, y1)
                area = width * height
                percent = area / msb_area

                if percent < 0.5: #intersecting < 50% of msb_area
                    final_dict_array.append(dict) # add the dict into the final array
                    dict_array.remove(dict) #removed to prevent dupes in final array
                    #TODO: TIDY UP AND OPTIMIZE
                    # Actually, from here, you can just remove those that intersect more than 0.5,
                    # those less than 0.5 can stay so it can be compared to each other
                else: #intersecting > 50% of msb_area (meaning too much overlap, hence, remove it)
                    dict_array.remove(dict)

        return final_dict_array
    
    #function to find intersecting coordinates
    def calculateIntersection(self, a0, a1, b0, b1):
        if a0 >= b0 and a1 <= b1: # Contained
            intersection = a1 - a0
        elif a0 < b0 and a1 > b1: # Contains
            intersection = b1 - b0
        elif a0 < b0 and a1 > b0: # Intersects right
            intersection = a1 - b0
        elif a1 > b1 and a0 < b1: # Intersects left
            intersection = b1 - a0
        else: # No intersection (either side)
            intersection = 0

        return intersection
