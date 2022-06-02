import tkinter
from tkinter import messagebox
import datetime
import json
import socket
from _thread import *

e = datetime.datetime.now()
# This code is to hide the main tkinter window
root = tkinter.Tk()
root.withdraw()

ServerSideSocket = socket.socket()
# Change host to server machine's ipv4 address when allowing connection to ESP32 or other external devices
host = '0.0.0.0'
port = 2004
ThreadCount = 0

microwave_list = []


def multi_threaded_client(connection):
    connection.send(str.encode('Server is working:'))
    while True:
        data = connection.recv(2048)
        if not data:
            break
    connection.close()


try:
    ServerSideSocket.bind((host, port))
except socket.error as e:
    print(str(e))
print('Socket is listening..')

'''
 If there's an error on the next line for Windows, try:
 > open CMD
 > netstat -ano | findstr :2004 
 > tskill <PID from result, rightmost column>
'''
ServerSideSocket.listen(5)

while True:
    Client, address = ServerSideSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(multi_threaded_client, (Client, ))
    ThreadCount += 1
    print('Thread Number: ' + str(ThreadCount))
    client_data = Client.recv(2048)
    print(client_data)
    info = json.loads(client_data.decode("utf-8").replace("'", '"'))
    #read json file

    # for val in info['MotionData']:
    #     if info['MotionData'][val] == "True":
    #         microwave_list.append(val + ": True")
            # messagebox.showerror("Alert", "Date of Alert: %s/%s/%s" % (e.day, e.month, e.year) + "\nTime of Alert: %s:%s:%s" % (e.hour, e.minute, e.second) + "\nMotion detected at: ")
    print(microwave_list)
    microwave_list.clear()
