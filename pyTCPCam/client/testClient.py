#run main
import multiprocessing
from audio.audioStream import AudioStream
from audio.audioProcessor import AudioProcessor
from clientTCP import ClientTCP
from video.videoEncoder import VideoEncoder
from video.videoProcessor import VideoProcessor
from video.videoStream import VideoStream

###############################
# Stats:
# Main Process: 
#   - RAM: 19MB for model and camera, +11MB for TCP client (reduced from 1.8GB)
#   - CPU: 1.5% on Intel i7-7700K (reduced from 15%)
#   - GPU: 0% on Nvidia GTX 1060
# Stream Process on 1920x1080 60FPS MP4: 
#   - RAM: 96MB - 107MB (reduced from 330MB)
#   - CPU: 14% - 16.1% on Intel i7-7700K
#   - GPU: 0% on Nvidia GTX 1060
# Inference Process
#   - RAM: 1.4GB - 1.7GB (reduced from 1.9GB)
#   - CPU: 13.4% - 13.9% on Intel i7-7700K
#   - GPU: 0.2% to 0.5% on Nvidia GTX 1060
# Audio Stream Process on 1 Second recording:
#   - RAM: 20MB - 25MB
#   - CPU: 0% on Intel i7-7700K
#   - GPU: 0% on Nvidia GTX 1060
# Audio Inference Process
#   - RAM: 180MB - 187MB
#   - CPU: 0.4% on Intel i7-7700K
#   - GPU: 0% on Nvidia GTX 1060

# have to find out why the increase in ram usage over time, memory leak?)
# Total reduced memory usage by 2.1GB~
# Total memory usage should be about 2GB with 1 Mic, 1 Camera, additional 20MB for each Mic or Camera
###############################

if __name__ == '__main__':
    camQueue = multiprocessing.Queue(1) #only put the latest image in the queue
    encQueue = multiprocessing.Queue(1)
    resultQueue = multiprocessing.Queue(1)
    audQueue = multiprocessing.Queue(1)

    imageModel = VideoProcessor(camQueue, encQueue, resultQueue).startAsProcess()
    # #start each video stream as a separate process
    videoStream0 = VideoStream("/dev/video0", 60, camQueue, False).startAsProcess()
    #videoStream0 = VideoStream("rtsp://admin:amarisipc1@192.168.1.64:554/Streaming/Channels/101/", 60, camQueue, True).startAsProcess()

    # #here the main process will encode and send thru tcp
    tcp = ClientTCP("Integrated Audio/Video Client", "192.168.1.199", 2004)
    #audio process
    audioStream0 = AudioStream(16000, audQueue, 11, "numpy_tf", 1).startAsProcess()
    audioProcessor = AudioProcessor('yamnet.h5', 1, audQueue, tcp).startAsProcess()

    #encoder and TCP
    videoEncoder0 = VideoEncoder(encQueue, resultQueue, 5, tcp).start()