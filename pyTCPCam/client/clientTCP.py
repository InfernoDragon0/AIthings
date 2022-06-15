from threading import Thread
import socket
import time
import jsonpickle

#connects to a TCP server to send image data over the network
#TODO test if a thread is better or worse?

class ClientTCP:
    def __init__(self, name, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port
        self.name = name
        self.completed = False
        self.data = None
        self.connect()

    def connect(self):
        try:
            self.socket.connect((self.host, self.port))
            self.socket.sendall(str.encode(f"HELLO:{self.name}"))
        except socket.error as e:
            print(e)
    
    # def start(self):
    #     Thread(target=self.sendData, args=()).start()
    #     return self
    
    def sendData(self,data):
        try:
            self.socket.sendall(str.encode(jsonpickle.encode(data)))
        except Exception as e:
            self.connect()
            print(f"reconnecting to server {e}")
            time.sleep(1)
            #just drop the frame if the connection failed, and restart the connection for the next frame

    def complete(self):
        self.completed = True

