"""[summary]
"""
import multiprocessing

import logging
import numpy as np

class AudioStream:
    """Class representing the microphone device.
    """

    class FormatNotSupportedError(Exception):
        pass

    def __init__(self, chunksize, audQueue, micIndex, listenType="raw", listenWindow=1):
        """[summary]
        Args:
            chunksize ([type]): [description]
        """
        self.completed = False
        self.SAMPLERATE = 16000
        self.CHUNK = chunksize
        self.frames = []
        self.ready = False
        self.listenType = listenType
        self.listenWindow = listenWindow
        self.completed = False
        self.micIndex = micIndex
        self.audQueue = audQueue

    
    def startAsProcess(self):
        print("Audio Stream Process started")
        self.camProcess = multiprocessing.Process(target=self.getAudio, args=(self.audQueue,))
        self.camProcess.start()
        return self

    def getFrames(self):
        return self.frames

    def complete(self):
        self.completed = True

    def getAudio(self,audQueue, filename="data"):
        import pyaudio
        """[summary]

        Args:
            listen_window ([type]): [description]
            blocking (bool, optional): [description]. Defaults to True.
            fmt (str, optional): [description]. Defaults to "raw".
            filename (str, optional): [description]. Defaults to "data".

        Raises:
            self.FormatNotSupportedError: [description]

        Returns:
            [type]: [description]
        """
        self.FORMAT = pyaudio.paInt16
        self.audio = pyaudio.PyAudio()
        try:
            self.CHANNELS = 2
            self.stream = self.audio.open(input_device_index=self.micIndex, format=self.FORMAT,channels=self.CHANNELS,rate=self.SAMPLERATE,input=True,frames_per_buffer=self.CHUNK)
            logging.info("Microphone successfully started")

        except Exception as e:
            
            self.CHANNELS = 1
            self.stream = self.audio.open(input_device_index=self.micIndex, format=self.FORMAT,channels=self.CHANNELS,rate=self.SAMPLERATE,input=True,frames_per_buffer=self.CHUNK)
            logging.info("Switching to mono channel microphone")
            logging.info("Microphone successfully started")

        while True:
            if self.completed:
                return

            self.recorder_numpy_tf(self.listenWindow)


    def recorder(self,listen_window):
        """[summary]

        Args:
            listen_window ([type]): [description]
        """
        self.frames = []
        for i in range(0,int(self.SAMPLERATE/self.CHUNK * listen_window)):
            data = self.stream.read(self.CHUNK)
            self.frames.append(data)
        self.ready = True

    def recorder_numpy(self,listen_window):
        """[summary]

        Args:
            listen_window ([type]): [description]
        """
        first = True
        for i in range(0,int(self.SAMPLERATE/self.CHUNK * listen_window)):
            data = self.stream.read(self.CHUNK)
            frame = np.frombuffer(data,dtype=np.int16)
            if self.CHANNELS == 2:
                frame = np.stack((frame[1::2],frame[::2]),axis=0)
            if first:
                self.frames = frame
                first = False
            else:
                self.frames = np.concatenate((self.frames,frame),axis=1)
        self.frames = np.transpose(self.frames)
        self.ready = True

    def recorder_numpy_tf(self,listen_window):

        first = True
        for i in range(0,int(self.SAMPLERATE/self.CHUNK * listen_window)):
            data = self.stream.read(self.CHUNK)
            frame = np.frombuffer(data,dtype=np.int16)
            frame = frame/32768.0
            if self.CHANNELS == 2:
                frame = np.stack((frame[1::2],frame[::2]),axis=0)
            if first:
                self.frames = frame
                first = False
            else:
                self.frames = np.concatenate((self.frames,frame),axis=1)
       
        if self.audQueue.empty():
            self.audQueue.put(self.frames)

    def get_all_numpy_tf(self,prev_audio_frame_array): #TODO check threading
        """
        """
        audio_data = self.stream.read(self.stream.get_read_available())
        audio_frame = np.frombuffer(audio_data,dtype=np.int16)
        audio_frame = audio_frame/32768.0 #Normalize for yamnet 
        if self.CHANNELS == 2:
            # Interleave stereo data into 2D numpy array
            audio_frame = np.stack((audio_frame[1::2],audio_frame[::2]),axis=0)

        if len(prev_audio_frame_array) ==0:
            audio_frame_array = audio_frame
        else:
            audio_frame_array = np.concatenate((prev_audio_frame_array,audio_frame),axis=1)
        
        return audio_frame_array