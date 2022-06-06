import tkinter
from tkinter import messagebox
import datetime
import socket
import struct
import jsonpickle
import cv2
from threading import Thread
#bind to all interfaces, can change this as needed
HOST = "0.0.0.0"
PORT = 2004
audio_list = []
def multi_threaded_client(connection):
    connection.send(str.encode('Server is working:'))
    while True:
        data = connection.recv(2048)
        try:
            info = data.decode("utf-8")

            print(info)
            for val in info["inferredData"]:
                if val["name"] == "speech" and info == "1":
                    if float(val["value"]) >= 0.5:
                        audio_list.append(val["name"]+":"+ val["value"])

            print(audio_list)
        except Exception as e:
            print(f"data not a json? {e}: data is {data}")
            #print("HELLO")
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
            #messagebox.showerror("Alert", "Date of Alert: %s/%s/%s" % (e.day, e.month, e.year) + "\nTime of Alert: %s:%s:%s" % (e.hour, e.minute, e.second)+ "\nNumber of people at location now: ")
            # for val in json["inferredData"]:
            #     audio_list.append(val["name"]+":"+ val["value"])
            # print(audio_list)
         
    