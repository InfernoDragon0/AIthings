import socket
import struct
import pickle
import cv2

#bind to all interfaces, can change this as needed
HOST = "0.0.0.0"
PORT = 8100

#using the socket to bind to server and accept each connection
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print("Server running")

    conn, addr = s.accept()

    with conn:
        print(f"Connected by {addr}")
        #while loop to keep receiving data
        while True:
            data = conn.recv(1024)
            print(data)
