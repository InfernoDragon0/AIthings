from data.baseInference import BaseInference


class ImageInference(BaseInference):
    def __init__(self):
        super().__init__()
        self.inferenceType = "dog"
        self.packetType = "Image"
        self.streamImage = False #set to true if want to send the image as well
        self.imageData = None

    def setStreamImage(self, stream):
        self.streamImage = stream

    def setImageData(self, data):
        self.imageData = data