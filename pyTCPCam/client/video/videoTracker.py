from concurrent.futures import process
import multiprocessing
import time


#unified to be able to change the sequence of these without any issues
class VideoTracker():
    def __init__(self, encQueue, trackedQueue, trackedResultQueue, resultQueue, maxFrameLoss, targetFPS, countQueue):
        self.completed = False
        self.ready = False
        self.resultQueue = resultQueue
        self.trackedQueue = trackedQueue
        self.trackedResultQueue = trackedResultQueue
        self.encQueue = encQueue
        self.currentID = 0
        self.maxFrameLoss = maxFrameLoss
        self.fps = 1/targetFPS
        self.countQueue = countQueue
        

    def startAsProcess(self):
        print("Tracking Process started")
        self.processorProcess = multiprocessing.Process(target=self.process, args=(self.encQueue, self.trackedQueue, self.trackedResultQueue, self.resultQueue, self.maxFrameLoss, self.fps, self.countQueue))
        self.processorProcess.start()
        return self
    
    def detectNew(self, obj):
        self.tracked[self.currentID] = obj
        self.leaving[self.currentID] = 0
        self.currentID += 1

    def removeOld(self, id):
        del self.tracked[id]
        del self.leaving[id]


    #encode loop to encode the latest frame received
    def process(self, encQueue, trackedQueue, trackedResultQueue, resultQueue, maxFrameLoss, fps, countQueue):
        import cv2
        from scipy.spatial import distance as dist
        import numpy as np
        self.tracked = {}
        self.leaving = {}
        self.result = None
        while True:
            if self.completed:
                return
            
            #take box data from the video processor
            if not encQueue.empty() and not resultQueue.empty():
                start = time.perf_counter()
                rects = resultQueue.get()
                processedImage = encQueue.get()

                if len(rects) == 0: #if nobody is inside anymore, remove everyone if they reach maxFrameLoss
                    for id in list(self.leaving.keys()):
                        self.leaving[id] += 1

                        if (self.leaving[id] >= maxFrameLoss):
                            self.removeOld(id)
                    continue #skip the rest of the steps

                #find centroids
                findCentroids = np.zeros((len(rects), 2), dtype="int")
                #print(rects)
                for i, faceData in enumerate(rects):
                    #print(faceData)
                    boxData = faceData["box"]
                    cX = int((boxData[0] + boxData[2]) / 2.0)
                    cY = int((boxData[1] + boxData[3]) / 2.0)
                    findCentroids[i] = (cX, cY)
                
                if len(self.tracked) == 0: #if no people yet
                    for i in range(0, len(findCentroids)):
                        self.detectNew(findCentroids[i])
                else: #update the people
                    objectIDs = list(self.tracked.keys())
                    objectCentroids = list(self.tracked.values())

                    D = dist.cdist(np.array(objectCentroids), findCentroids)
                    rows = D.min(axis=1).argsort()
                    cols = D.argmin(axis=1)[rows]
                    usedCols = set()
                    usedRows = set()

                    for (row, col) in zip(rows, cols):
                        if row in usedRows or col in usedCols:
                            continue

                        objectID = objectIDs[row]
                        self.tracked[objectID] = findCentroids[col]
                        self.leaving[objectID] = 0

                        usedRows.add(row)
                        usedCols.add(col)

                    unusedRows = set(range(0, D.shape[0])).difference(usedRows)
                    unusedCols = set(range(0, D.shape[1])).difference(usedCols)
                    if D.shape[0] >= D.shape[1]:
                        for row in unusedRows:
                            objectID = objectIDs[row]
                            self.leaving[objectID] += 1

                            if self.leaving[objectID] >= self.maxFrameLoss:
                                self.removeOld(objectID)

                    else:
                        for col in unusedCols:
                            self.detectNew(findCentroids[col])
                    

                    for i, trackable in self.tracked.items():
                        processedImage = cv2.putText(processedImage, f"ID: {i}", trackable, cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255), 2)

                    if trackedQueue.empty():
                        trackedQueue.put(processedImage)

                    if trackedResultQueue.empty():
                        trackedResultQueue.put(rects)
                    
                    if countQueue.empty():
                        countQueue.put(self.currentID)

                    #cv2.imshow("tracker", processedImage)
                    #cv2.waitKey(1)
                    #if (self.fps - (end-start) > 0):
                        #time.sleep(self.fps - (end-start))\
                end = time.perf_counter()
                print(f"tracking time: {end - start}")
                if (fps - (end - start) > 0):
                    time.sleep(fps - (end - start))

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