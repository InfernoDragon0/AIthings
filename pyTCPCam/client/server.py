import tkinter
from tkinter import messagebox
import datetime
import socket
import struct
import jsonpickle
import cv2
import json
from threading import Thread
#bind to all interfaces, can change this as needed
HOST = "192.168.1.55"
PORT = 2004
audio_list = []
microwave_list = []
def multi_threaded_client(connection):
    microwave_list = []
    connection.send(str.encode('Server is working:'))
    while True:
        data = connection.recv(2048)
        changing = jsonpickle.encode(data)    
        jsonpickleData = jsonpickle.decode(changing)
        info = jsonpickleData.decode("utf-8")
        print(info)
        content = json.loads(info)
        print(content)
        #Check sensor
        # if info['packetType'] == "Sensor":
        #     for val in info['MotionData']:
        #             if info['MotionData'][val] == "True":
        #                 microwave_list.append("found")
        # elif info['packetType'] == "Audio":
            # for val in info["inferredData"]:
            #     if val["name"] == "speech":
            #         if float(val["value"]) >= 0.5:
            #             audio_list.append(val["name"]+":"+ val["value"])        
        # print(microwave_list)
    

        # print(audio_list)
        # except Exception as e:
        #     print(f"data not a json? {e}: data is {data}")
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

