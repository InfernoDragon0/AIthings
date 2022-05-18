import imagezmq
from threading import Thread

#connects to a TCP server to send image data over the network
#TODO!!! as there is no wait time, tcp client may try to keep sending the exact same frame resulting in 300fps being sent
#this may affect the network performance if there is alot of clients sending at max speed
#solution: apply wait time (check the performance before applying wait time)

class ClientTCP:
    def __init__(self, name, encoder, host, port, pubSub):
        self.encoder = encoder
        self.sender = imagezmq.ImageSender(connect_to=f"tcp://{host}:{port}") #As Client
        self.name = name
        self.completed = False
        self.current_frame = self.encoder.getEncodedFrame() #get initial frame

        if (pubSub):
            self.sender = imagezmq.ImageSender(connect_to=f"tcp://0.0.0.0:{port}", REQ_REP=False) #As Publisher
    
    def start(self):
        Thread(target=self.sendData, args=()).start()
        return self
    
    def sendData(self):
        while True:
            if self.completed:
                return
            if (self.current_frame == self.encoder.getEncodedFrame()):
                continue
            
            self.current_frame = self.encoder.getEncodedFrame()
            try:
                self.sender.send_jpg(self.name, self.current_frame)
            except Exception as e:
                print(e)
    
    def complete(self):
        self.completed = True

