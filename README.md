# Integrated client
## Client Side

### Prerequisites & Installation
- Python 3+
- OpenCV (cv2)
- SimpleJPEG
- pyTorch
- Tensorflow
- jsonpickle
- Model files for the inferencers

Running on the Jetson Nano, the preconfigured conda environment will have all the required prerequisites.

### Steps to run the client
- ```conda activate testenv```
- cd to ```client``` directory
- ```python testClient.py```

### Check your mic index
Run ```python micCheck.py``` from client directory to check your mic index

### Folders & Files
- ```audio``` contains the code required to read from an audio source and run inference
- ```data``` contains the class files required for transferring data over the network
- ```video``` contains the code required to read from a video source and run inference
- ```models``` yolov5 required dependencies
- ```sensor``` contains the code required to read from different sensor sources
- ```utils``` yolov5 wrapper dependencies
- ```yamnet``` yamnet tensorflow required dependencies
- ```client.py``` deprecated client
- ```testClient.py``` main client to run the integrated system
- ```yolo_wrapper.py``` dependency to load models for image inferencing
- ```yolov5.py``` yolov5 wrapper dependencies
- ```micCheck.py``` to check your mic index

### Configuration files
Located in ```client/config.json```, you may change the config file to fit your use case
- ```py/object``` should not be changed
- ```videoSource``` should be set to the video source(s) that are connected to the client
- ```videoModel``` should be set to the model file
- ```videoDebug``` can be set to true to provide a preview on the client. (do not set to true on headless mode, does not work)
- ```targetFPS``` the target FPS to read the camera at
- ```audioSource``` the mic index(s) of the audio source to read from. Check your mic index using micCheck.py. 
- ```audioModel``` should be set to the model file
- ```audioListenTime``` the amount of time to listen from the source before inferencing
- ```audioListenType``` the type of audio source to infer
- ```audioBitRate``` the bitrate of the audio
- ```tcpHost/tcpPort``` the host and port of the TCP server
- ```tcpName``` the name of the client
- ```tcpSendTime``` the maximum rate that the TCP client should send data to the server (5 = 5 combined images, audio, sensor per second)
- ```audioInferenceType/videoInferenceType``` what to infer
- ```maxFrameLoss``` the amount of frames before dropping an object for the object tracker

### Further documentation
visit the [Confluence Page](https://sititp-atas-e.atlassian.net/wiki/spaces/SIA/overview?homepageId=98512)
