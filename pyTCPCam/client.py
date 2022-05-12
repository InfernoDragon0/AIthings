import cv2
import imagezmq

#bind to all interfaces to publish in the pub/sub
SUB = "0.0.0.0"
HOST = "192.168.1.213"
PORT = 8100
NAME = "one"
#clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sender = ""

#connects to a TCP server to send image data over the network
#the image data is pickled (into a byte array stream)
#then the data is sent through the network with the dataSize (LENGTH as a LONG)
#in addition to sending the actual image data dataToServer (byte array stream)

def main():
    #socketConnect() #connect to socket
    #startAsPublisher()
    startAsClient()
    startCam() #start the camera

#connects to the socket provided HOST and PORT
#def socketConnect():
    #print("Socket connect")
    #clientSocket.connect((HOST, PORT))
def startAsPublisher():
    global sender
    sender = imagezmq.ImageSender(connect_to=f"tcp://{SUB}:{PORT}", REQ_REP=False)

def startAsClient():
    global sender
    sender = imagezmq.ImageSender(connect_to=f"tcp://{HOST}:{PORT}")

#starts the camera and sends data from VideoCapture(0) (webcam)
def startCam():
    vid = cv2.VideoCapture(0)
    while(True):
        ret, frame = vid.read()

        #dump the frames into byte array stream
        # dataToServer = pickle.dumps(frame)

        #size of the byte array stream as Long
        # dataSize = struct.pack("L", len(dataToServer))

        #call send through TCP server
        # sendData(dataSize + dataToServer) 
        sendData(frame)
        #DEBUG PREVIEW can remove this if client doesnt need to preview
        cv2.imshow('clientFrame', frame) 
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    vid.release()
    #DEBUG PREVIEW can be removed if client doesnt need to preview
    cv2.destroyAllWindows()

#try sending the frame over the network
#if not connected, try connecting and retry sending
def sendData(frame):
    try:
        sender.send_image(NAME, frame)
        # clientSocket.sendall(frame)
    except Exception as e:
        print(e)
        #socketConnect()
        #sendData(frame) #recursive, or just drop the frame

#run as main things
if __name__ == '__main__':
    main()