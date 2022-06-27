import tkinter
from tkinter import messagebox
import socket
import struct
import jsonpickle
import cv2
from threading import Thread
import simplejpeg
import time
import csv
import numpy as np
import tensorflow as tf
import datetime 
HOST = "0.0.0.0"
PORT = 2004
audio_list = []
microwave_list = []
image_list = []
image_counter = 0
def audio_class_names(class_map_csv):
#   Read the class name definition file and return a list of strings.
  if tf.is_tensor(class_map_csv):
    class_map_csv = class_map_csv.numpy()
  with open(class_map_csv) as csv_file:
    reader = csv.reader(csv_file)
    next(reader)   # Skip header
    return np.array([display_name for (_, _, display_name) in reader])

def multi_threaded_client(connection):
    connection.send(str.encode('Server is working:'))
    while True:
        flag_image = 0
        flag_audio = 0
        flag_sensor = 0
        data = connection.recv(64000)
        try:
            dataPickle = jsonpickle.decode(data)
            f = open("output.txt","a")
            #global inference data check
            if dataPickle.inferredData is None or len(dataPickle.inferredData) == 0: 
                print(f"{dataPickle.packetType}: No object of interest in image")
                continue
            if dataPickle.packetType == 'Audio':
                packetTime_audio = datetime.datetime.now() 
                print(f"Audio data received: {dataPickle.inferredData} at time {packetTime_audio}")
                #Get audio name
                audio_name = audio_class_names("yamnet_class_map.csv")
                #Check audio sound is human and check for value that is great or equal to 10
                for val in range(0,67):
                    for i in range(0,4):
                        if audio_name[val] == dataPickle.inferredData[i]['name']:
                            if float(dataPickle.inferredData[i]['value']) >= 0.5:       
                                print("Human sound detected")
                                print("Audio data received:" + dataPickle.inferredData[i]['name'] +" and the value is "+ dataPickle.inferredData[i]['value'] +" at time " +str(packetTime_audio),file=f)
                                flag_audio += 1           
                                break
                        break
            elif dataPickle.packetType == 'Image':
                face_counter = len(dataPickle.inferredData)
                packetTime_image = datetime.datetime.now()

                print(f"Number of faces received: {len(dataPickle.inferredData)} at time {packetTime_image}")
                if dataPickle.imageData is not None:
                    decodedImage = simplejpeg.decode_jpeg(dataPickle.imageData, colorspace='BGR')
                    cv2.imshow("server", decodedImage)
                    cv2.waitKey(1)
                #Check for faces
                if len(dataPickle.inferredData) >= 1:
                    print("Human is detected")
                    print("Number of faces received:" +len(dataPickle.inferredData) +" at time " +str(packetTime_image))

                    flag_image += 1
            elif dataPickle.packetType == 'Sensor':
                packetTime_sensor = datetime.datetime.now()
                print(f"Sensor data received: {dataPickle.inferredData} at time {packetTime_sensor}")
                #Sensor check
                if dataPickle.inferredData == 1:
                    print("Sensor data received: "+ dataPickle.inferredData+ " at time "+str(packetTime_sensor))
                    flag_sensor += 1
            else:
                print(f"New data type found: {dataPickle.packetType}")
            #check flag
            if flag_audio == 1 and flag_image== 1 or flag_sensor== 1 and flag_audio == 1 or flag_image == 1 and flag_sensor == 1 or flag_audio == 1 and flag_image == 1 and flag_sensor == 1:
                #alert will pop up
                if flag_image == 1:
                    messagebox.showerror("Alert", "Date of Alert: %s/%s/%s" % (e.day, e.month, e.year) + "\nTime of Alert: %s:%s:%s" % (e.hour, e.minute, e.second)+ "\nNumber of people at location now: "+ face_counter)
                else:
                    messagebox.showerror("Alert", "Date of Alert: %s/%s/%s" % (e.day, e.month, e.year) + "\nTime of Alert: %s:%s:%s" % (e.hour, e.minute, e.second)+ "\nNumber of people at location now: not found \nAudio and Sensor detected people")
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