# import jsonpickle
import time
#Base class to be inherited for other inferences
class BaseInference():
    def __init__(self):
        self.packetType = "Base" #set this packet type depending on which data you send
        self.inferredData = [] #an array of Objects provided by the inferences
        self.timestamp = time.time() #set the timestamp to the time of initialization OR time of inference
    
    #adds object data into the inference arrray
    def addData(self, data):
        self.inferredData.append(data)

    #convert the data to json for sending to server
    #def asJson(self):
        # return jsonpickle.encode(self)
        #SAMPLE: {packetType:"Base", inferredData:[{data:x, data2:y}, {data:x, data2:y}]}