import socket
import struct
import pickle
import cv2
from threading import Thread
#bind to all interfaces, can change this as needed
HOST = "0.0.0.0"
PORT = 8100

def multi_threaded_client(connection):
    connection.send(str.encode('Server is working:'))
    while True:
        data = connection.recv(2048)
        print(data)
        if not data:
            break
    connection.close()

#using the socket to bind to server and accept each connection
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print("Server running")
    while True:
        conn, addr = s.accept()
        Thread(target=multi_threaded_client, args=(conn, )).start()

