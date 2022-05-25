"""[summary]
"""
import pyaudio
import wave
import logging
import numpy as np

class Microphone:
    """Class representing the microphone device.
    """

    class FormatNotSupportedError(Exception):
        pass


    def __init__(self,chunksize):
        """[summary]

        Args:
            chunksize ([type]): [description]
        """
        try:
            self.CHANNELS = 2
            self.SAMPLERATE = 16000
            self.CHUNK = chunksize
            self.FORMAT = pyaudio.paInt16
            self.frames = []
            self.audio = pyaudio.PyAudio()
            self.stream = self.audio.open(format=self.FORMAT,channels=self.CHANNELS,rate=self.SAMPLERATE,input=True,frames_per_buffer=self.CHUNK)
            logging.info("Microphone successfully started")

        except Exception as e:
            self.CHANNELS = 1
            self.SAMPLERATE = 16000
            self.CHUNK = chunksize
            self.FORMAT = pyaudio.paInt16
            self.frames = []
            self.audio = pyaudio.PyAudio()
            self.stream = self.audio.open(format=self.FORMAT,channels=self.CHANNELS,rate=self.SAMPLERATE,input=True,frames_per_buffer=self.CHUNK)
            logging.info("Switching to mono channel microphone")
            logging.info("Microphone successfully started")


    def get_audio(self,listen_window,blocking=True,fmt="raw",filename="data"):
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
        
        
        if blocking:
            if fmt == "numpy":
                return self.recorder_numpy(listen_window)

            if fmt == "numpy_tf":
                return self.recorder_numpy_tf(listen_window)
            if fmt == "raw":
                raw_data = self.recorder(listen_window)
                return raw_data
            elif fmt == "wav":
                raw_data = self.recorder(listen_window)
                with wave.open(filename + ".wav","wb") as wavefile:
                    wavefile.setframerate(self.SAMPLERATE)
                    wavefile.setnchannels(self.CHANNELS)
                    wavefile.setsampwidth(self.audio.get_sample_size(self.FORMAT))
                    wavefile.writeframes(b''.join(raw_data))
                    return filename + ".wav"
            else:
                raise self.FormatNotSupportedError("Supported Formats are 'raw' and 'wav'")


        else:
            #TODO: Supoort Non-blocking mode with multithread
            pass


    def recorder(self,listen_window):
        """[summary]

        Args:
            listen_window ([type]): [description]
        """
        self.frames = []
        for i in range(0,int(self.SAMPLERATE/self.CHUNK * listen_window)):
            data = self.stream.read(self.CHUNK)
            self.frames.append(data)

        return self.frames

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
                frames_array = frame
                first = False
            else:
                frames_array = np.concatenate((frames_array,frame),axis=1)
        frames_array = np.transpose(frames_array)
        return frames_array


    def recorder_numpy_tf(self,listen_window):

        first = True
        for i in range(0,int(self.SAMPLERATE/self.CHUNK * listen_window)):
            data = self.stream.read(self.CHUNK)
            frame = np.frombuffer(data,dtype=np.int16)
            frame = frame/32768.0
            if self.CHANNELS == 2:
                frame = np.stack((frame[1::2],frame[::2]),axis=0)
            if first:
                frames_array = frame
                first = False
            else:
                frames_array = np.concatenate((frames_array,frame),axis=1)
        

        

        return frames_array


    def get_all_numpy_tf(self,prev_audio_frame_array):
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

