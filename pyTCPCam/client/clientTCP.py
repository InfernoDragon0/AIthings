from threading import Thread
import socket
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
    
    def start(self):
        Thread(target=self.sendData, args=()).start()
        return self
    
    def sendData(self):
        try:
            self.socket.sendall(str.encode(jsonpickle.encode(self.data)))
        except Exception as e:
            self.connect()
            print(f"reconnecting to server {e}")
            self.sendData(self)
    
    def addData(self, data):
        self.data = data

    def complete(self):
        self.completed = True

