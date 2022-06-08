import cv2
import multiprocessing

from video.videoStream import VideoStream

if __name__ == "__main__":
    
    stream = VideoStream(0).startAsProcess()
    stream.startDebug()