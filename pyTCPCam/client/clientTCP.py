import imagezmq
from threading import Thread

#connects to a TCP server to send image data over the network
#TODO!!! as there is no wait time, tcp client may try to keep sending the exact same frame resulting in 300fps being sent
#this may affect the network performance if there is alot of clients sending at max speed
#solution: apply wait time (check the performance before applying wait time)

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
            try:
                self.sender.send_jpg(self.name, frame)
            except Exception as e:
                print(e)
    
    def complete(self):
        self.completed = True

