import tkinter
from tkinter import messagebox
import datetime
import json
import jsonpickle
#show current date and time
e = datetime.datetime.now()
# This code is to hide the main tkinter window
root = tkinter.Tk()
root.withdraw()

import socket
import os
from _thread import *
ServerSideSocket = socket.socket()
host = '127.0.0.1'
port = 2004
ThreadCount = 0
inputfile_audio = open('audio.json')
inputfile_image = open('image.json')

#json_test = jsonpickle.decode('baseInference.cpython-38.pyc')
json_audio = json.load(inputfile_audio)
json_image = json.load(inputfile_image)
audio_list = []

try:
    ServerSideSocket.bind((host, port))
except socket.error as e:
    print(str(e))
print('Socket is listening..')
ServerSideSocket.listen(5)
def multi_threaded_client(connection):
    connection.send(str.encode('Server is working:'))
    while True:
        data = connection.recv(2048)
        if not data:
            break
    connection.close()
while True:
    Client, address = ServerSideSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(multi_threaded_client, (Client, ))
    ThreadCount += 1
    print('Thread Number: ' + str(ThreadCount))
    data = Client.recv(2048)
    info = data.decode("utf-8")
    #read json file
    
    for val in json_audio["inferredData"]:
        if val["name"] == "speech" and info == "1":
            if float(val["value"]) >= 0.5:
                audio_list.append(val["name"]+":"+ val["value"])
                messagebox.showerror("Alert", "Date of Alert: %s/%s/%s" % (e.day, e.month, e.year) + "\nTime of Alert: %s:%s:%s" % (e.hour, e.minute, e.second)+ "\nNumber of people at location now: ")
    print(audio_list)
ServerSideSocket.close()