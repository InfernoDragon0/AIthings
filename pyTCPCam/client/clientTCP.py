import cv2
import imagezmq
import simplejpeg
import imutils
from pyTCPCam.client.clientStream import ClientStream

#set to the HOST:PORT to connect to
HOST = "192.168.1.53"
PORT = 8100

#set the name of this camera / multicam
NAME = "two"

#ImageZMQ sender init
sender = imagezmq.ImageSender(connect_to=f"tcp://{HOST}:{PORT}")

#connects to a TCP server to send image data over the network
#for optimization:
#in addition, encode the openCV data to jpeg
#in addition, reduce the jpeg image quality
#TODO in addition, reduce the size of the jpeg before sending
#in addition, only sends the latest frame that could be processed to the server
#TODO in addition, move to publisher to remove blocking latency
#TODO in addition, server shall process each stream in a separate thread to reduce latency
#TODO in addition, client shall process each stream in a separate thread to reduce latency
#in addition, FPS counter

#starts the camera and sends data received from clientStream
#clientStream is started on a separate thread for each camera
def main():
    cam0 = ClientStream(0).start()
 
    #TODO move this into another thread
    while(True):
        frame = cam0.getFrame()
        jpg_buffer = simplejpeg.encode_jpeg(frame, quality=40, colorspace='BGR') #40 has minimal difference to the eyes

        #call send through server
        sendData(jpg_buffer)

        #DEBUG PREVIEW can remove this if client doesnt need to preview
        cv2.imshow('clientFrame', frame) 
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    #DEBUG PREVIEW can be removed if client doesnt need to preview
    cv2.destroyAllWindows()
    cam0.complete()
    
#try sending the frame over the network
def sendData(frame):
    try:
        sender.send_jpg(NAME, frame)
    except Exception as e:
        print(e)

#run as main things
if __name__ == '__main__':
    main()