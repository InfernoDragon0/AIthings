import cv2
import imagezmq
import simplejpeg
import imutils
from clientEncoder import ClientEncoder
from clientStream import ClientStream
from threading import Thread

#set to the HOST:PORT to connect to
HOST = "192.168.1.53"
PORT = 8100

#set the name of this camera / multicam
NAME = "two"

#ImageZMQ sender init
#sender = imagezmq.ImageSender(connect_to=f"tcp://{HOST}:{PORT}")

#connects to a TCP server to send image data over the network
#for optimization:
#in addition, encode the openCV data to jpeg
#in addition, reduce the jpeg image quality
#TODO in addition, reduce the size of the jpeg before sending
#in addition, only sends the latest frame that could be processed to the server
#TODO in addition, move to publisher to remove blocking latency
#TODO in addition, server shall process each stream in a separate thread to reduce latency
#in addition, client shall process each stream in a separate thread to reduce latency
#in addition, FPS counter

#starts the camera and sends data received from clientStream
#clientStream is started on a separate thread for each camera
#clientEncoder will encode and do optimizations to the image before sending
#tcp client will always try to send the latest frame encoded
#TODO due to race conditions, tcp client may try to 
class ClientTCP:
    def __init__(self, name, encoder, host, port):
        self.encoder = encoder
        self.sender = imagezmq.ImageSender(connect_to=f"tcp://{host}:{port}")
        self.name = name
        self.completed = False
    
    def start(self):
        Thread(target=self.sendData, args=()).start()
        return self
    
    def sendData(self):
        while True:
            if self.completed:
                return

            frame = self.encoder.getEncodedFrame()
            if (frame == None): continue #skip the frame if it is still being prepared
            
            try:
                self.sender.send_jpg(self.name, frame)
            except Exception as e:
                print(e)
    
    def complete(self):
        self.completed = True

def main():
    cam0 = ClientStream(0).start()
    cam0Encoder = ClientEncoder(cam0).start()
    tcpClient0 = ClientTCP("Cam 0", cam0Encoder, HOST, PORT).start()
 
    #TODO test first, then move this into another thread
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

#run as main things
if __name__ == '__main__':
    main()
