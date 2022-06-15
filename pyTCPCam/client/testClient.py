#run main
import multiprocessing
from clientTCP import ClientTCP
from video.videoEncoder import VideoEncoder
from video.videoProcessor import VideoProcessor
from video.videoStream import VideoStream

###############################
# Stats:
# Main Process: 
#   - RAM: 19MB for model and camera, +11MB for TCP client (from 1.8GB due to imports shared between sub-processes)
#   - CPU: 1.5% on Intel i7-7700K (reduced from 15%)
#   - GPU: 0% on Nvidia GTX 1060
# Stream Process on 1920x1080 60FPS MP4: 
#   - RAM: 96MB - 107MB (from 330MB due to imports shared between sub-processes)
#   - CPU: 14% - 16.1% on Intel i7-7700K
#   - GPU: 0% on Nvidia GTX 1060
# Inference Process
#   - RAM: 1.4GB - 1.7GB (from 1.9GB due to imports shared between sub-processes)
#   - CPU: 13.4% - 13.9% on Intel i7-7700K
#   - GPU: 0.2% to 0.5% on Nvidia GTX 1060
# have to find out why the increase in ram usage over time, memory leak?)
# Total reduced memory usage by 2.1GB~
###############################

if __name__ == '__main__':
    camQueue = multiprocessing.Queue(1) #only put the latest image in the queue
    encQueue = multiprocessing.Queue(1)
    resultQueue = multiprocessing.Queue(1)

    imageModel = VideoProcessor(camQueue, encQueue, resultQueue).startAsProcess()
    #start each video stream as a separate process
    #videoStream0 = VideoStream("vlc.mp4", 60, camQueue, False).startAsProcess()
    videoStream0 = VideoStream("rtsp://admin:amarisipc1@192.168.1.64:554/Streaming/Channels/101/", 60, camQueue, True).startAsProcess()

    #here the main process will encode and send thru tcp
    tcp = ClientTCP("Integrated Inference Client", "127.0.0.1", 8100)
    videoEncoder0 = VideoEncoder(encQueue, resultQueue, 5, tcp).start()