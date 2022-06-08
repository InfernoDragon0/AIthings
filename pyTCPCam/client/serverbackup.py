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
        info = data.decode("utf-8")
        print(info)
        # for val in info:
        #     print(val["packetType"])
        #     print(val["inferredData"])
        # info = json.loads(data.decode("utf-8").replace("'", '"'))
        # print(info)
        # for val in info["packetType"]:
            # print(val["packetType"])

        # elif info["inferredData"]:
        #     print("Data found")
        # content = json.loads(info)
        # print(content)
        #Check sensor
        # if content['packetType'] == "Sensor":
        #     for val in content['MotionData']:
        #             if content['MotionData'][val] == "True":
        #                 microwave_list.append("found")
        # if info['packetType'] == "Audio":
        #     for val in info["inferredData"]:
        #         if val["name"] == "speech":
        #             if float(val["value"]) >= 0.5:
        #                 audio_list.append(val["name"]+":"+ val["value"])        
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

