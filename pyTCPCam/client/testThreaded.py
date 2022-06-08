import cv2

from video.videoStream import VideoStream

if __name__ == "__main__":
    stream = VideoStream(0).start()
    stream.startDebug()