from audio.audioStream import AudioStream
from audio.audioProcessor import AudioProcessor
from data.imageInference import ImageInference
from video.videoStream import VideoStream
from video.videoEncoder import VideoEncoder
from video.videoProcessor import VideoProcessor
from clientTCP import ClientTCP

#NETWORK CONFIG
HOST = "192.168.1.53"
PORT = 8100
startAsPublisher = False #set to True for PUBSUB. Server must run in PUBSUB mode as well

########################################################################
# Optimizations done:
# 1. Encoded the openCV data to JPEG
# 2. Reduce the jpeg image quality to 40
# 3. Only sends the latest frame that could be processed to the server
# 4. OpenCV image stream is processed in a separate thread
# 5. Inferencing is done in another separate thread
# 6. JPEG Encoding is processed in another separate thread
# 7. Processed frames are sent to the server in another separate thread
########################################################################

########################################################################
#TODO in addition, reduce the size of the jpeg before sending
#TODO the threads doesnt exit(?)
########################################################################

#Client class to start multiple cameras
class Client():
    def __init__(self, cameraId):
        #init video stream. The sequence of these can be swapped at any time but the stream must start first
        self.videoStream = VideoStream(cameraId).start()
        self.videoProcessor = VideoProcessor(self.videoStream).start()
        self.videoEncoder = VideoEncoder(self.videoProcessor).start()

        #DEBUG PREVIEW can remove this if client doesnt need to preview
        self.videoDebug = self.videoProcessor.startDebug()

        #init audio stream
        self.audioStream = AudioStream(16000, "numpy_tf", 1).start()
        self.audioProcessor = AudioProcessor('yamnet.h5', 1, self.audioStream).start()

        #init sensor stream #or maybe no need?

        #init TCP connection
        #self.sendVideoStream = False
        #self.videoTCP = ClientTCP(f"Cam {cameraId}", self.videoEncoder, HOST, PORT,startAsPublisher).start() #TODO change to overall TCP connection

    
    def stop(self):
        self.videoStream.complete()
        self.videoProcessor.complete()
        self.videoEncoder.complete()

        self.audioStream.complete()
        self.audioProcessor.complete()


#run main code
def main():
    #run as many clients as you want as long as it is one camera per Client object
    cam0 = Client(0) #can swap in with a .mp4 file to test without camera

    # while(True): #show for client 0
    #     if keyboard.is_pressed('q'):
    #         break

    #cam0.stop()
    #sys.exit(0)

#run main
if __name__ == '__main__':
    main()