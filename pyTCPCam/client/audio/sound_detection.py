import numpy as np
import os
from microphone import Microphone
import yamnet.params as yamnet_params
import yamnet.yamnet as yamnet_model
import yamnet.metadata as metadata
import logging
from operator import itemgetter
import time

def load_model():
    params = yamnet_params.Params()
    yamnet = yamnet_model.yamnet_frames_model(params)
    yamnet.load_weights('yamnet.h5')
    yamnet_classes = np.array([x['name'] for x in metadata.CAT_META])
    return yamnet,yamnet_classes


def infer(audio_data,model,yamnet_classes):
    audio_data = np.transpose(audio_data)
    if len(audio_data.shape) > 1:
        audio_data = np.mean(audio_data,axis=1)


    scores,embeddings,spectrogram = model(audio_data)

    top_N = 5
    mean_scores = np.mean(scores,axis=0)
    top_class_indices = np.argsort(mean_scores)[::-1][:top_N]

    results = []
    total_scores = 0
    for i in top_class_indices:
        pred_class = yamnet_classes[i].replace("'","")
        pred = (pred_class,mean_scores[i])
        total_scores += mean_scores[i]
        results.append(pred)

    unknown_class_score = 1.0 - total_scores
    results.append(("unknown",unknown_class_score))
    

    return sorted(results,key=itemgetter(1),reverse=True)

    
def listen(listen_window = 1):
    """
    Function that listens from the latest <listen_window> amount of seconds from
    the microphone and prints the results to console. Used for unit testing.

    Args:
        microphone (_type_): _description_
        listen_window (int, optional): _description_. Defaults to 1.
    """
    microphone = Microphone(chunksize=16000)
    model,class_names = load_model()
    while True:
        print("Listening")
        audio_data = microphone.get_audio(listen_window,fmt="numpy_tf")
        results = infer(audio_data,model,class_names)
        print(results)


if __name__ == "__main__":
    
    listen(listen_window=1)
    # print(np.array([x['name'] for x in metadata.CAT_META]))
