import imagezmq
from threading import Thread

#connects to a TCP server to send image data over the network
#TODO as there is no wait time, tcp client may try to keep sending the exact same frame resulting in 300fps being sent
#if it does not affect performance, does not matter.


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
            #this check slows it down, probably because the TCP server is sending at 10x the encoding speed
            # if (self.current_frame == self.encoder.getEncodedFrame()):
            #     continue
            if (not self.encoder.ready):
                continue
            
            self.encoder.ready = False
            self.current_frame = self.encoder.getEncodedFrame()
            try:
                self.sender.send_jpg(self.name, self.current_frame)
            except Exception as e:
                print(e)
    
    def complete(self):
        self.completed = True

