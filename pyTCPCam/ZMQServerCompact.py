import cv2
import imagezmq
import simplejpeg
import time 
#the server subscribes to the PUB:PORT clients with pub/sub
PUB = "192.168.1.109"

#OR host a server as HOST:PORT and wait for clients
HOST = "0.0.0.0"
PORT = 8100

#open the image hub MQ using PUB SUB
image_hub = imagezmq.ImageHub(open_port=f'tcp://{PUB}:{PORT}', REQ_REP=False)
startAsSubscriber = False

#sub to one publisher
def startAsSub():
    global image_hub
    image_hub = imagezmq.ImageHub(open_port=f'tcp://{PUB}:{PORT}', REQ_REP=False)


#get from many clients
def startAsServer():
    global image_hub
    image_hub = imagezmq.ImageHub(open_port=f'tcp://{HOST}:{PORT}')

def main():
    #for one user
    start_time = time.time()
    counter = 0
    fpsText = "0"

    while True:
        clientName, imagex = image_hub.recv_jpg() #use this image to do things related to the AI
        image_hub.send_reply(b'OK') #send reply before anything else
        image = simplejpeg.decode_jpeg( imagex, colorspace='BGR') #quality reduction 
        
        # time when we finish processing for this frame
        counter += 1
        if (time.time() - start_time) > 1:
            fpsText = str(counter / (time.time() - start_time))
            start_time = time.time()
            counter = 0

        cv2.putText(image, fpsText, (7,70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
        cv2.imshow(clientName, image) # 1 window for each
        cv2.waitKey(1)
        

if __name__ == '__main__':
    if (startAsSubscriber):
        startAsSub()
    else:
        startAsServer()
    main()
