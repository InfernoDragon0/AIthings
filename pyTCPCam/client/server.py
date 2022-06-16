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
        data = connection.recv(2048)
        info = data.decode("utf8").replace("'", "\"")
        if is_json(info) == True: 
            dict = json.loads(data.decode("utf8").replace("'", "\""))
            
            # Checking if Camera and microphone loading
            if dict["inferredData"] == None or dict["inferredData"] != []:
                print("Loading Camera and Audio")
            else:
                #Check timestamp
                # print(dict)
                # checktimestamp(time)
                # dt_object = datetime.fromtimestamp(dict["timestamp"])
                # dt_objectadd =dt_object + timedelta(seconds=0.4)
                # print(dict["packetType"]+": "+dt_object)
                # if dt_object <= dt_objectadd:
                #     test.append(dict)
                test.append(dict)     
            for val in range(0,len(test)):
                if test[val]["packetType"] == "Image":
                    counter_face = 0
                    for i in test[val]["inferredData"]:
                        if i["class"] == "face":
                            counter_face += 1
                    f = open("output.txt", "a")
                    print("Number of face = "+ counter_face + " Time: "+ int(datetime.fromtimestamp(test[val]["timestamp"])), file=f)
                    f.close()
                elif test[val]["packetType"] == "Audio":
                    f = open("output.txt", "a")
                    print("Audio sound and value = "+ str(test[val]["inferredData"]) + " Time: "+ int(datetime.fromtimestamp(test[val]["timestamp"])), file=f)
                    f.close()
                elif test[val]["packetType"] == "Sensor":
                    f = open("output.txt", "a")
                    print("Sensor value = "+ str(test[val]["inferredData"]) + " Time: "+ int(datetime.fromtimestamp(test[val]["timestamp"])), file=f)
                    f.close()
            test = []

        else:
            f = open("error.txt", "a")
            print(info, file=f)
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

    

