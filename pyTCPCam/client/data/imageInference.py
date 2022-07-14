from data.baseInference import BaseInference


class ImageInference(BaseInference):
    def __init__(self, inferenceType):
        super().__init__()
        self.inferenceType = inferenceType
        self.packetType = "Image"
        self.streamImage = False #set to true if want to send the image as well
        self.imageData = None
        self.objectCount = 0

    def setStreamImage(self, stream):
        self.streamImage = stream

    def setImageData(self, data):
        self.imageData = data