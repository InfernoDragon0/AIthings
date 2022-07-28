# Integrated Client
## Server Side
Run the server before running the client

### Prerequisites & Installation
- Python 3+
- OpenCV (cv2)
- jsonpickle
- SimpleJPEG
- Tensorflow

### Steps to run the server
- Change the PORT to fit your client/server
- Leave HOST as ```0.0.0.0``` unless binding on specific interface
- Client should follow IP of the server
- cd to ```client``` directory
- ```python server.py```

### Folders / Files
- ```server.py``` main server file
- ```yamnet_class_map.csv``` The file to check the audio identification type
- ```data``` data folder to link to the client side
