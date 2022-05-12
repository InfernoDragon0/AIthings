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
    conn, addr = s.accept()
    #empty variables init
    data = b''
    dataSize = struct.calcsize("L")

    with conn:
        print(f"Connected by {addr}")
        #while loop to keep receiving data
        while True:
            #receive the full data before continuing
            while len(data) < dataSize:
                data += conn.recv(1024)

            #split the size and actual data 
            clientDataSize = data[:dataSize]
            data = data[dataSize:]
            tempSize = struct.unpack("L", clientDataSize)[0]

            #ensure that the frame data received is actually the same length as the length Long we sent over
            while len(data) < tempSize:
                data += conn.recv(1024)

            frameSize = data[:tempSize]
            data = data[tempSize:]
            
            #pickle load the frame from the byte array
            frame = pickle.loads(frameSize)
            cv2.imshow('serverFrame', frame)
            cv2.waitKey(1)
