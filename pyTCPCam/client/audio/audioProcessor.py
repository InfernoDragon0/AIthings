from time import sleep
import numpy as np
from data.audioInference import AudioInference
import yamnet.params as yamnet_params
import yamnet.yamnet as yamnet_model
import yamnet.metadata as metadata
from operator import itemgetter
from threading import Thread
import time

class AudioProcessor():
    def __init__(self, fileName, listenWindow, audioStream, tcp): #loading takes a long time, separate thread?
        self.params = yamnet_params.Params()
        self.yamnet = yamnet_model.yamnet_frames_model(self.params)
        self.yamnet.load_weights(fileName)
        self.yamnet_classes = np.array([x['name'] for x in metadata.CAT_META])
        self.inferredResults = []
        #self.timestamp = time.time()
        #self.tcpTime = 1
        self.tcp = tcp
        self.listenWindow = listenWindow
        self.audioStream = audioStream
        self.completed = False

    def start(self):
        Thread(target=self.listen, args=()).start()
        return self
    
    def complete(self):
        self.completed = True
    
    def listen(self):
        """
        Function that listens from the latest <listen_window> amount of seconds from
        the microphone and prints the results to console. Used for unit testing.

        Args:
            microphone (_type_): _description_
            listen_window (int, optional): _description_. Defaults to 1.
        """
        while True:
            if self.completed:
                return
            
            if (not self.audioStream.ready):
                continue

            print("Listening")
            audio_data = np.transpose(self.audioStream.getFrames())
            if len(audio_data.shape) > 1:
                audio_data = np.mean(audio_data,axis=1)

            scores,embeddings,spectrogram = self.yamnet(audio_data)

            top_N = 5
            mean_scores = np.mean(scores,axis=0)
            top_class_indices = np.argsort(mean_scores)[::-1][:top_N]

            results = []
            total_scores = 0
            for i in top_class_indices:
                pred_class = self.yamnet_classes[i].replace("'","")
                pred = (pred_class,mean_scores[i])
                total_scores += mean_scores[i]
                results.append(pred)

            unknown_class_score = 1.0 - total_scores
            results.append(("unknown",unknown_class_score))
            

            self.inferredResults = sorted(results,key=itemgetter(1),reverse=True)
            self.audioStream.ready = False
            #and send the data over tcp, every x seconds [TODO to send only when alert or something]
            #since audio is already every 1 second no need a separate timer to check
            #if self.timestamp + self.tcpTime < time.time():
                #self.timestamp = time.time()
            self.audioInference = AudioInference()
            for k,v in enumerate(self.inferredResults):
                self.audioInference.addInferenceData(v[0], str(v[1]))

            self.tcp.addData(self.audioInference)
            self.tcp.start()
            
            print(self.inferredResults)