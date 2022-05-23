from threading import Thread

#TODO AI stuff in another thread, before the ClientEncoder. AI to tell ClientEncoder to encode (probably with a variable) when ready

class ClientProcessor():
    def __init__(self, encoder):
        self.completed = False
        self.encoder = encoder
        self.processedFrame = self.encoder.encodedFrame #TODO apply the AI here one time if possible
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

            self.processedFrame = None #TODO do some AI stuff here
            self.ready = True

    def asInferenceObject(self): #can remove if not needed
        return {"x": 123, "y": 234, "confidence": 1, "inferred": "Person"}

    #get the latest inferenced frame
    def getProcessedFrame(self):
        return self.processedFrame

    #end the thread
    def complete(self):
        self.completed = True