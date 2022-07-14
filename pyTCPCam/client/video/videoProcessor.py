import multiprocessing
import time
import cv2
import subprocess
import os

#unified to be able to change the sequence of these without any issues
class VideoProcessor():
    def __init__(self, camQueue, encQueue, resultQueue, videoModel):
        self.completed = False
        self.ready = False
        self.camQueue = camQueue
        self.encQueue = encQueue
        self.resultQueue = resultQueue
        self.videoModel = videoModel

    def startAsProcess(self):
        print("Processor Process started")
        self.processorProcess = multiprocessing.Process(target=self.process, args=(self.camQueue, self.encQueue, self.resultQueue, self.videoModel))
        self.processorProcess.start()
        return self

    #encode loop to encode the latest frame received
    def process(self, camQueue, encQueue, resultQueue, videoModel):
        from yolo_wrapper import Process #it is a sin that has to be done

        self.processedFrame = None
        self.result = None
        self.model = Process(device=0, weights=videoModel)
        while True:
            if self.completed:
                return
            
            #self.processedFrame is used to get the current frame
            #infer the image with the model to get the result
            if not camQueue.empty():
                image = camQueue.get()
                
                if image is not None:
                    start = time.perf_counter()
                    self.result = self.model.inference_json_result(image)

                    #Setting up constants
                    ####PATH = "../../tensorrtxbuilder/yolov5_inferenceonly/"                    
                    DIR_CURRENT = os.path.dirname(os.path.dirname(os.path.abspath(os.getcwd()))) #/amaris/
                    #print(DIR_CURRENT)
                    #going to tensorrtxbuilder/yolov5_inferenceonly
                    DIR_YOLO5INF = os.path.join(DIR_CURRENT, "tensorrtxbuilder", "yolov5_inferenceonly")
                    #print(DIR_YOLO5INF)


                    CMD_INF = ["./yolov5", "-i", "atasv3.engine"]
                    PROCESS = str.encode("process_img\n")
                    ## save image to folder inferenceonly folder first
                    cv2.imwrite(os.path.join(DIR_YOLO5INF, "temp.jpg"), image)
                    ## use subprocess to run the .engine to read
                    pipe = subprocess.Popen(CMD_INF, stdin=subprocess.PIPE, stderr=subprocess.PIPE, cwd=DIR_YOLO5INF, shell=True)
                    pipe.stdin.write(PROCESS)
                    pipeout, pipeer = pipe.communicate()
                    print(pipeout)


                    if(len(self.result) > 1): #no need to bother with just 1 item in array
                        self.result = self.nms(self.result)
                    #print(self.result)

                    #drawing the bounding boxes based on the result on the image
                    image = self.model.draw_box_xyxy(image, self.result)
                    self.setProcessedFrame(image)
                    end = time.perf_counter()
                    #print(f"perf counter is {end-start}")

                    if encQueue.empty() and resultQueue.empty():
                        encQueue.put(image)
                        resultQueue.put(self.result)
                    
                    #cv2.imshow("processor", image)
                    #cv2.waitKey(1)
                    #if (self.fps - (end-start) > 0):
                        #time.sleep(self.fps - (end-start))
            # else:
            #     time.sleep(self.fps)

    #unified to reduce changes
    def getFrame(self):
        return self.processedFrame

    def setProcessedFrame(self, img):
        self.processedFrame = img

    #end the thread
    def complete(self):
        self.completed = True
    
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

                if percent > 0.5: #intersecting > 50%, hence remove dict from array
                    dict_array.remove(dict)
                #those < 50% can keep to be checked with the rest that are not eliminated

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
