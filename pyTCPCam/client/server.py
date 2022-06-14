import tkinter
from tkinter import messagebox
import datetime
import socket
import struct
import jsonpickle
import cv2
import json
from threading import Thread
import base64
import binascii

HOST = "192.168.1.55"
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
def is_base64(s):
    try:
        base64.decodestring(s)
        return True
    except binascii.Error:
        return False

def multi_threaded_client(connection):
    microwave_list = []
    connection.send(str.encode('Server is working:'))
    while True:
        data = connection.recv(2048)
        info = data.decode("utf8").replace("'", "\"")
        if is_json(info) == True: 
            dict = json.loads(data.decode("utf8").replace("'", "\""))
            # Checking for Image value
            if dict["packetType"] == "Image":
                # Camera and microphone loading
                if dict["inferredData"] == None:
                    print("Loading Camera and Audio")
                # Load finish
                else:
                    if dict["inferredData"] != []:
                        for val in dict["inferredData"]:
                            counter_face = 0
                            if val["class"] == "face":
                                counter_face += 1


                        image_list.append(counter_face)
                    
                    print(image_list)
            # Checking for audio
            elif dict["packetType"] == "Audio":
                audio_list.append(dict["inferredData"])
                print(audio_list)                    
            # Checking for Sensor value
            elif dict["packetType"] == "Sensor":
                microwave_list.append(dict["inferredData"])

        else:
            print(info)                
            
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
