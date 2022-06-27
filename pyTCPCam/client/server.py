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
image_counter = 0


def audio_class_names(class_map_csv):
    #   Read the class name definition file and return a list of strings.
    if tf.is_tensor(class_map_csv):
        class_map_csv = class_map_csv.numpy()
    with open(class_map_csv) as csv_file:
        reader = csv.reader(csv_file)
        next(reader)  # Skip header
        return np.array([display_name for (_, _, display_name) in reader])


def multi_threaded_client(connection):
    connection.send(str.encode('Server is working:'))
    while True:
        data = connection.recv(64000)
        try:
            flag_image = 0
            flag_audio = 0
            flag_sensor = 0
            dataPickle = jsonpickle.decode(data)
            f = open("output.txt", "a")
            # global inference data check
            if dataPickle['inferredData'] is None or len(dataPickle['inferredData']) == 0:
                print(f"{dataPickle.packetType}: No object of interest in image")
                continue
            if dataPickle['packetType'] == 'Audio':
                packetTime_audio = datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')
                print(f"Audio data received: {dataPickle.inferredData} at time {packetTime_audio}")
                # Get audio name
                audio_name = audio_class_names("yamnet_class_map.csv")
                # Check audio sound is human and check for value that is great or equal to 10
                for val in range(0, 67):
                    for i in range(0, 4):
                        if audio_name[val] == dataPickle.inferredData[i]['name']:
                            if float(dataPickle.inferredData[i]['value']) >= 0.5:
                                print("Human sound detected")
                                print("Audio data received: " + dataPickle.inferredData[i][
                                    'name'] + " and the value is " + dataPickle.inferredData[i][
                                          'value'] + " at time " + str(packetTime_audio), file=f)
                                audio_soundname = dataPickle.inferredData[i]['name']
                                audio_value = dataPickle.inferredData[i]['value']
                                flag_audio = 1
                                break
                        break
            elif dataPickle['packetType'] == 'Image':
                face_counter = len(dataPickle.inferredData)
                packetTime_image = datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')

                print(f"Number of faces received: {len(dataPickle.inferredData)} at time {packetTime_image}")
                if dataPickle.imageData is not None:
                    decodedImage = simplejpeg.decode_jpeg(dataPickle.imageData, colorspace='BGR')
                    cv2.imshow("server", decodedImage)
                    cv2.waitKey(1)
                # Check for faces
                if len(dataPickle.inferredData) >= 1:
                    print("Human is detected")
                    print("Number of faces received: " + str(len(dataPickle.inferredData)) + " at time " + str(
                        packetTime_image), file=f)
                    flag_image = 2
            elif dataPickle['packetType'] == 'Sensor':
                packetTime_sensor = datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')
                print(f"Sensor data received: {dataPickle['inferredData']} at time {packetTime_sensor}")
                # Sensor check
                if dataPickle['inferredData'][0]['name'] == "ultrasonic":
                    if dataPickle['inferredData'][0]['value'] == 1:
                        print("Sensor data received: " + str(dataPickle['inferredData'][0]['name']) + " at time " + str(packetTime_sensor), file=f)
                        flag_sensor = 1
                        # sensor_value = dataPickle['inferredData']
                        print("flag sensor "+ str(flag_sensor))
            else:
                print(f"New data type found: {dataPickle.packetType}")
            # check flag

            # print("Flag Audio " + str(flag_audio) + " Flag image " + str(flag_image) + " Flag sensor " + str(flag_sensor))
            if (flag_audio + flag_image + flag_sensor) >= 2:
                image = 'Not detected'
                audio = 'Not detected '
                sensor = 'Not detected'
                # alert will pop up
                packetTime_alert = datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')
                if flag_image == 2:
                    image = "Number of people at location now: " + str(len(dataPickle.inferredData))
                if flag_audio == 1:
                    audio = "Audio sound " + audio_soundname + " value of sound " + audio_value
                if flag_sensor == 1:
                    sensor = "Sensor " + sensor_value

                messagebox.showerror("Alert",
                                     "Date of Alert and Time: " + packetTime_alert + "\nImage: " + image + "\nAudio: " + audio + "\nSensor: " + sensor)
            f.close()
        except Exception as e:
            if len(data) != 0:
                print(data)
                print(f"Error reading data json {e}")

            f = open("error.txt", "a")
            print(data, file=f)
            f.close()

        if not data:
            break


# using the socket to bind to server and accept each connection
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print("Server running")
    while True:
        conn, addr = s.accept()
        Thread(target=multi_threaded_client, args=(conn,)).start()