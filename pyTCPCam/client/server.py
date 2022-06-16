import tkinter
from tkinter import messagebox
import socket
import struct
import jsonpickle
import cv2
import json
from threading import Thread
import base64
from datetime import datetime, timedelta
import simplejpeg

HOST = "0.0.0.0"
PORT = 2004
audio_list = []
microwave_list = []
image_list = []
counter_face = 0
def is_json(myjson):
  try:
    json.loads(myjson)
  except ValueError as e:
    return False
  return True

def validjson(myvalue):
    try:
        json.loads(myvalue)
    except ValueError as e:
        return False
    return True
# def checktimestamp(time):

def multi_threaded_client(connection):
    test = []
    connection.send(str.encode('Server is working:'))
    while True:
        data = connection.recv(16000)
        try:
            dataPickle = jsonpickle.decode(data)

            #global inference data check
            if dataPickle.inferredData is None or len(dataPickle.inferredData) == 0:
                print(f"{dataPickle.packetType}: No data available for inference")
                continue
            
            f = open("output.txt", "a") #this is taxing if you keep opening and closing in the while loop

            if dataPickle.packetType == 'Audio':
                print(f"Audio data received: {dataPickle.inferredData} at time {dataPickle.timestamp}")

            elif dataPickle.packetType == 'Image':
                print(f"Number of faces received: {len(dataPickle.inferredData)} at time {dataPickle.timestamp}")
                if dataPickle.imageData is not None:
                    decodedImage = simplejpeg.decode_jpeg(dataPickle.imageData, colorspace='BGR')
                    cv2.imshow("server", decodedImage)
                    cv2.waitKey(1)
            
            elif dataPickle.packetType == 'Sensor':
                print(f"Sensor data received: {dataPickle.inferredData} at time {dataPickle.timestamp}")
            
            else:
                print(f"New data type found: {dataPickle.packetType}")
            
            f.close()

        
        except Exception as e:
            print(f"Error reading data json {e}")
        
            f = open("error.txt", "a")
            print(data, file=f)
            f.close()          
            
        if not data:
            break

#using the socket to bind to server and accept each connection
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print("Server running")
    while True:
        conn, addr = s.accept()
        Thread(target=multi_threaded_client, args=(conn, )).start()

    

