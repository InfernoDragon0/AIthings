from threading import Thread

#unified to be able to change the sequence of these without any issues
class VideoProcessor():
    def __init__(self, stream):
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

            self.processedFrame = self.stream.getFrame() #TODO do some AI stuff here
            self.ready = True

    def asInferenceObject(self): #can remove if not needed
        return {"x": 123, "y": 234, "confidence": 1, "inferred": "Person"}

    #unified to reduce changes
    def getFrame(self):
        return self.processedFrame

    #end the thread
    def complete(self):
        self.completed = True