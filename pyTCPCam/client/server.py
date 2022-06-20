import tkinter
from tkinter import messagebox
import socket
import struct
import jsonpickle
import cv2
from threading import Thread
from datetime import datetime
import simplejpeg
import time
import csv
import numpy as np
import tensorflow as tf
HOST = "0.0.0.0"
PORT = 2004
audio_list = []
microwave_list = []
image_list = []
counter_face = 0
def audio_class_names(class_map_csv):
#   Read the class name definition file and return a list of strings.
  if tf.is_tensor(class_map_csv):
    class_map_csv = class_map_csv.numpy()
  with open(class_map_csv) as csv_file:
    reader = csv.reader(csv_file)
    next(reader)   # Skip header
    return np.array([display_name for (_, _, display_name) in reader])

def multi_threaded_client(connection):
    test = []
    flag_count = 0
    connection.send(str.encode('Server is working:'))
    while True:
        data = connection.recv(64000)
        try:
            currenttiming = datetime.time()
            dataPickle = jsonpickle.decode(data)

            #global inference data check
            if dataPickle.inferredData is None or len(dataPickle.inferredData) == 0: 
                print(f"{dataPickle.packetType}: No data available for inference")
                continue


            if dataPickle.packetType == 'Audio':
                print(f"Audio data received: {dataPickle.inferredData} at time "+ str(datetime.fromtimestamp(int(dataPickle.timestamp))))
                #Get audio name
                audio_name = audio_class_names("yamnet_class_map.csv")
                
                #Check audio sound is human and check for value that is great or equal to 10
                for val in range(0,67):
                    if audio_name[val]:
                        if dataPickle.inferredData.value >= 0.5:       
                            print(dataPickle.inferredData.name + " and value is " + dataPickle.inferredData.value)           
            elif dataPickle.packetType == 'Image':
                counter = 0
                print(f"Number of faces received: {len(dataPickle.inferredData)} at time " + str(datetime.fromtimestamp(int(dataPickle.timestamp))))
                if dataPickle.imageData is not None:
                    decodedImage = simplejpeg.decode_jpeg(dataPickle.imageData, colorspace='BGR')
                    cv2.imshow("server", decodedImage)
                    cv2.waitKey(1)

                print("FPS: ", 1.0 / (time.time() - dataPickle.timestamp))
            elif dataPickle.packetType == 'Sensor':
                print(f"Sensor data received: {dataPickle.inferredData} at time "+ str(datetime.fromtimestamp(int(dataPickle.timestamp))))
            
            else:
                print(f"New data type found: {dataPickle.packetType}")
        
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
    audio_name = audio_class_names("yamnet_class_map.csv")
    for val in range(0,67):
        if audio_name[val]:
            print(audio_name[val])
    # while True:
    #     conn, addr = s.accept()
    #     Thread(target=multi_threaded_client, args=(conn, )).start()