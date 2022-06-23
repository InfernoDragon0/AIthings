#run main
import multiprocessing
from video.videoProcessor import VideoProcessor
from video.videoStream import VideoStream

###############################
# Stats: (MAIN STREAM, Channel 101)
# 1280 x 720
#   - FPS: 20
#       - Camera Capture Time: 0.0000 seconds per frame
#       - Inference Time: 0.0000 seconds per frame
#   - FPS: 40
#       - Camera Capture Time: 0.0000 seconds per frame
#       - Inference Time: 0.0000 seconds per frame
#   - FPS: 60
#       - Camera Capture Time: 0.02 - 0.07 seconds per frame
#       - Inference Time: 0.20 - 0.30 seconds per frame
# 1920 x 1080
#   - FPS: 20
#       - Camera Capture Time: 0.0000 seconds per frame
#       - Inference Time: 0.0000 seconds per frame
#   - FPS: 40
#       - Camera Capture Time: 0.0000 seconds per frame
#       - Inference Time: 0.0000 seconds per frame
#   - FPS: 60
#       - Camera Capture Time: 0.0000 seconds per frame
#       - Inference Time: 0.0000 seconds per frame
# 2048 x 1536
#   - FPS: 20
#       - Camera Capture Time: 0.0000 seconds per frame
#       - Inference Time: 0.0000 seconds per frame
#   - FPS: 40
#       - Camera Capture Time: 0.0000 seconds per frame
#       - Inference Time: 0.0000 seconds per frame
#   - FPS: 60
#       - Camera Capture Time: 0.0000 seconds per frame
#       - Inference Time: 0.0000 seconds per frame
###############################

if __name__ == '__main__':
    camQueue = multiprocessing.Queue(1) #only put the latest image in the queue
    encQueue = multiprocessing.Queue(1)
    resultQueue = multiprocessing.Queue(1)

    rtspSrc = "rtsp://admin:amarisipc1@10.1.1.10:554/Streaming/Channels/101/"

    imageModel = VideoProcessor(camQueue, encQueue, resultQueue).startAsProcess()
    
    #comment out each videostream each test
    #videoStream0 = VideoStream(f"rtspsrc location={rtspSrc} latency=0 ! rtph264depay ! h264parse ! nvv4l2decoder ! nvvidconv ! video/x-raw, format=BGRx, width=1280, height=720 ! videorate ! 'video/x-raw(memory:NVMM),framerate=20/1'", 20, camQueue, True).startAsProcess()
    #videoStream0 = VideoStream(f"rtspsrc location={rtspSrc} latency=0 ! rtph264depay ! h264parse ! nvv4l2decoder ! nvvidconv ! video/x-raw, format=BGRx, width=1920, height=1080 ! videorate ! 'video/x-raw(memory:NVMM),framerate=20/1'", 20, camQueue, True).startAsProcess()
    #videoStream0 = VideoStream(f"rtspsrc location={rtspSrc} latency=0 ! rtph264depay ! h264parse ! nvv4l2decoder ! nvvidconv ! video/x-raw, format=BGRx, width=2048, height=1536 ! videorate ! 'video/x-raw(memory:NVMM),framerate=20/1'", 20, camQueue, True).startAsProcess()
    #videoStream0 = VideoStream(f"rtspsrc location={rtspSrc} latency=0 ! rtph264depay ! h264parse ! nvv4l2decoder ! nvvidconv ! video/x-raw, format=BGRx, width=3840, height=2160 ! videorate ! 'video/x-raw(memory:NVMM),framerate=20/1'", 20, camQueue, True).startAsProcess()
    videoStream0 = VideoStream(f"rtspsrc location={rtspSrc} latency=0 ! rtph264depay ! h264parse ! nvv4l2decoder ! nvvidconv ! video/x-raw, format=BGRx, width=1280, height=720 ! videoconvert ! video/x-raw,format=BGR ! appsink", 60, camQueue, True).startAsProcess()
    videoStream0 = VideoStream("rtsp://admin:amarisipc1@10.1.1.10:554/Streaming/Channels/101/", 60, camQueue, True).startAsProcess()
