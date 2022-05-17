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

#sub to one publisher
def startAsSubscriber():
    image_hub = imagezmq.ImageHub(open_port=f'tcp://{PUB}:{PORT}', REQ_REP=False)
    while True:
        clientName, image = image_hub.recv_image() #use this image to do things related to the AI
        cv2.imshow(clientName, image) # 1 window only
        cv2.waitKey(1)

#get from many clients
def startAsServer():
    image_hub = imagezmq.ImageHub(open_port=f'tcp://{HOST}:{PORT}')

    #for one user
    start_time = time.time()
    counter = 0

    while True:
        clientName, imagex = image_hub.recv_jpg() #use this image to do things related to the AI
        image_hub.send_reply(b'OK') #send reply before anything else
        image = simplejpeg.decode_jpeg( imagex, colorspace='BGR') #quality reduction 
        
        # time when we finish processing for this frame
        counter += 1
        if (time.time() - start_time) > 1:
            cv2.putText(image, str(counter / (time.time() - start_time)), (7,70), cv2.FONT_HERSHEY_SIMPLEX, 3, (100, 255, 0), 3, cv2.LINE_AA)
            start_time = time.time()
            counter = 0

        cv2.imshow(clientName, image) # 1 window for each
        cv2.waitKey(1)
        

if __name__ == '__main__':
    #startAsSubscriber()
    startAsServer()
