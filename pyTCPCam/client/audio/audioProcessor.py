import multiprocessing
from time import sleep
import numpy as np
from data.audioInference import AudioInference
from operator import itemgetter

class AudioProcessor():
    def __init__(self, fileName, listenWindow, audQueue, tcp): #loading takes a long time, separate thread?
        self.fileName = fileName
        #self.timestamp = time.time()
        #self.tcpTime = 1
        self.tcp = tcp
        self.listenWindow = listenWindow
        self.completed = False
        self.audQueue = audQueue

    def startAsProcess(self):
        print("Audio Processor Process started")
        self.camProcess = multiprocessing.Process(target=self.listen, args=(self.fileName, self.audQueue,self.tcp))
        self.camProcess.start()
        return self
    
    def complete(self):
        self.completed = True
    
    def listen(self, fileName, audQueue, tcp): 
        import yamnet.params as yamnet_params #scary but necessary
        import yamnet.yamnet as yamnet_model
        import yamnet.metadata as metadata
        """
        Function that listens from the latest <listen_window> amount of seconds from
        the microphone and prints the results to console. Used for unit testing.

        Args:
            microphone (_type_): _description_
            listen_window (int, optional): _description_. Defaults to 1.
        """
        self.params = yamnet_params.Params()
        self.yamnet = yamnet_model.yamnet_frames_model(self.params)
        self.yamnet.load_weights(fileName)
        self.yamnet_classes = np.array([x['name'] for x in metadata.CAT_META])
        self.inferredResults = []

        while True:
            if self.completed:
                return
            
            if audQueue.empty():
                sleep(0.2) #todo change to fps
                continue

            print("Listening")
            audio_data = np.transpose(audQueue.get())
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
            #and send the data over tcp, every x seconds [TODO to send only when alert or something]
            #since audio is already every 1 second no need a separate timer to check
            #if self.timestamp + self.tcpTime < time.time():
                #self.timestamp = time.time()
            self.audioInference = AudioInference()
            for k,v in enumerate(self.inferredResults):
                self.audioInference.addInferenceData(v[0], str(v[1]))

            tcp.sendData(self.audioInference)
            
            print(self.inferredResults)