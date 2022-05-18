from clientEncoder import ClientEncoder
from clientStream import ClientStream
from clientTCP import ClientTCP
import cv2
import sys

#NETWORK CONFIG
HOST = "192.168.1.53"
PORT = 8100

########################################################################
# Optimizations done:
# 1. Encoded the openCV data to JPEG
# 2. Reduce the jpeg image quality to 40
# 3. Only sends the latest frame that could be processed to the server
# 4. OpenCV image stream is processed in a separate thread
# 5. JPEG Encoding is processed in another separate thread
# 6. Processed frames are sent to the server in another separate thread
#in addition, FPS counter
########################################################################

########################################################################
#TODO !!! TCP CLIENT IS SENDING AT MAX SPEED, INCLUDING DUPLICATES, FIX SOON
#TODO in addition, server shall process each stream in a separate thread to reduce latency (maybe)
#TODO in addition, move to publisher to remove blocking latency (maybe)
#TODO in addition, reduce the size of the jpeg before sending
#TODO convert main() to use a for loop to start multi cam
#TODO the threads doesnt exit(?)
########################################################################

#starts the camera and sends data received from clientStream
#clientStream is started on a separate thread for each camera
#clientEncoder will encode and do optimizations to the image before sending
#tcp client will always try to send the latest frame encoded
def main():
    cam0 = ClientStream(0).start()
    cam0Encoder = ClientEncoder(cam0).start()
    tcpClient0 = ClientTCP("Cam 0", cam0Encoder, HOST, PORT).start()
 
    while(True):
        #DEBUG PREVIEW can remove this if client doesnt need to preview
        cv2.imshow('clientFrame', cam0.getFrame()) 
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    #DEBUG PREVIEW can be removed if client doesnt need to preview
    cv2.destroyAllWindows()

    cam0.complete()
    cam0Encoder.complete()
    tcpClient0.complete()
    sys.exit(0)

#run main
if __name__ == '__main__':
    main()