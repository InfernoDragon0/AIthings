from time import sleep
from audio.audioStream import AudioStream
from audio.audioProcessor import AudioProcessor
from data.imageInference import ImageInference
from video.videoStream import VideoStream
from video.videoEncoder import VideoEncoder
from video.videoProcessor import VideoProcessor
from clientTCP import ClientTCP
import multiprocessing
import cv2

#NETWORK CONFIG
HOST = "127.0.0.1"
PORT = 8100

########################################################################
# Optimizations done:
# 1. Encoded the openCV data to JPEG
# 2. Reduce the jpeg image quality to 40
# 3. Only sends the latest frame that could be processed to the server
# 4. OpenCV image stream is processed in a separate thread
# 5. Inferencing is done in another separate thread
# 6. JPEG Encoding is processed in another separate thread
# 7. The client is separated into two processes, one for camera, one for audio
########################################################################

########################################################################
#TODO the flag is used to tell the process to stop. Not implemented yet.
########################################################################

#Client class to start multiple cameras
class Client():
    def __init__(self, cameraId):
        self.flag = multiprocessing.Value("I", True)
        self.camProcess = multiprocessing.Process(target=self.runCam, args=(cameraId,self.flag))
        self.camProcess.start()
        #self.camProcess.join()

        #init TCP connection
        #self.sendVideoStream = False
        #self.videoTCP = ClientTCP(f"Cam {cameraId}", self.videoEncoder, HOST, PORT,startAsPublisher).start() #TODO change to overall TCP connection

    def runCam(self, cameraId, flag):
        #init video stream
        #self.tcp = ClientTCP(f"Cam {cameraId}", HOST, PORT)
        self.videoStream = VideoStream(cameraId).start()
        #self.videoProcessor = VideoProcessor(self.videoStream).start()
        #self.videoEncoder = VideoEncoder(self.videoProcessor, self.tcp).start()

        #DEBUG PREVIEW can remove this if client doesnt need to preview
        #self.videoDebug = self.videoStream.startDebug()

        # while (flag.value):
        #     pass

        # print("Video stream terminating")
        # self.videoStream.complete()
        # self.videoProcessor.complete()
        # self.videoEncoder.complete()

    def stop(self):
        self.camProcess.terminate()
        

class AudioClient():
    def __init__(self, cameraId):
        self.flag = multiprocessing.Value("I", True)
        self.audioProcess = multiprocessing.Process(target=self.runAudio, args=(cameraId, self.flag))
        self.audioProcess.start()

    def runAudio(self, cameraId, flag):
        #init audio stream
        self.tcp = ClientTCP(f"Audio {cameraId}", HOST, PORT)
        self.audioStream = AudioStream(16000, "numpy_tf", 1).start()
        self.audioProcessor = AudioProcessor('yamnet.h5', 1, self.audioStream, self.tcp).start()

        # while (flag.value):
        #     pass
    
        # print("Audio stream terminating")
        # self.audioStream.complete()
        # self.audioProcessor.complete()

    def stop(self):
        self.audioProcess.terminate()

#run main code
def main():
    #run as many clients as you want as long as it is one camera per Client object
    #cam0 = Client(0) #can swap in with a .mp4 file to test without camera
    #cam0 = Client("/dev/video0")
    #audio0 = AudioClient(0)
    cap = cv2.VideoCapture("/dev/video0")

    while True:
        ret,frame = cap.read()
        if ret:
            cv2.imshow("Test",frame)
        else:
            print("Program broken")
            break

        cv2.waitKey(1)

    # while(True): #show for client 0
    #     if keyboard.is_pressed('q'):
    #         break

    #sleep(200)
    #cam0.stop()
    #audio0.stop()
    #sys.exit(0)

#run main
if __name__ == '__main__':
    main()