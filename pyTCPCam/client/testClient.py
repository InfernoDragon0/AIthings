#run main
import multiprocessing
from video.videoProcessor import VideoProcessor
from video.videoStream import VideoStream


if __name__ == '__main__':
    camQueue = multiprocessing.Queue(1) #only put the latest image in the queue
    imageModel = VideoProcessor(camQueue).startAsProcess()
    #start each video stream as a separate process
    videoStream0 = VideoStream("vlc.mp4", 60, camQueue, True).startAsProcess()