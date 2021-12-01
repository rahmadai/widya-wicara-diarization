import torch
import os
import soundfile as sf
import numpy as np
from pyannote.audio.utils.signal import Binarize
from pyannote.audio.utils.signal import Peak
from scipy.spatial.distance import cdist

#Path Audio Ouput
OUTPUT_WAV_DIR = '/home/hamz/speaker-diarization/env/tmp'


#Model Parameter
MODEL_DIR_VAD = 'pyannote/pyannote-audio'
MODEL_VAD = 'sad_dihard'
MODEL_DIR_OSD = 'pyannote/pyannote-audio'
MODEL_OSD = 'ovl_dihard'
MODEL_DIR_SCD = 'pyannote/pyannote-audio'
MODEL_SCD = 'scd_dihard'
MODEL_DIR_EMB = 'pyannote/pyannote-audio'
MODEL_EMB = 'emb'
MODEL_DIR_DIA = 'pyannote/pyannote-audio'
MODEL_DIA = 'dia_ami'

#Voice Activity Detection
class VAD:
    def __init__(self, model_path=MODEL_DIR_VAD, model=MODEL_VAD):
        try:
            self.sad = torch.hub.load(model_path, model)
            print("Load VAD Model Sucessfull!")

        except:
            print("Load VAD Model Failed!")

    def process(self, file_path):
        self.file_path = file_path
        self.audio, self.sr = sf.read(self.file_path['audio'])
        self.sad_scores = self.sad(file_path)
        self.binarize = Binarize(offset=0.52, onset=0.52, log_scale=True, 
                    min_duration_off=0.1, min_duration_on=0.1)
        self.result = self.binarize.apply(self.sad_scores, dimension=1)
        self.segmentSize = len(self.result.for_json()['content'])
        self.segmentTime = self.result.for_json()['content']

    def getSegmentSize(self):
        return self.result
        
    def outputWAV(self, segment):
        start = self.segmentTime[segment]['start']
        end = self.segmentTime[segment]['end']
        self.output_path = "SegmentVAD-{}.wav".format(segment)
        self.output_path = os.path.join(OUTPUT_WAV_DIR, self.output_path)
        sf.write(self.output_path, self.audio[int(start*self.sr):int(end*self.sr)], self.sr, 'PCM_24')


#Overlap Speech Detection
class OSD:
    def __init__(self, model_path=MODEL_DIR_OSD, model=MODEL_OSD):
        try:
            self.osd = torch.hub.load(model_path, model)
            print("Load OSD Model Sucessfull!")

        except:
            print("Load OSD Model Failed!")
    
    def process(self, file_path):
        self.file_path = file_path
        self.audio, self.sr = sf.read(self.file_path['audio'])
        self.osd_scores = self.osd(file_path)
        self.binarize = Binarize(offset=0.52, onset=0.52, log_scale=True, 
                    min_duration_off=0.05, min_duration_on=0.1)
        self.overlap = self.binarize.apply(self.osd_scores, dimension=1)
        self.segmentSize = len(self.overlap.for_json()['content'])
        self.segmentTime = self.overlap.for_json()['content']

    def outputWAV(self, segment):
        start = self.segmentTime[segment]['start']
        end = self.segmentTime[segment]['end']
        self.output_path = "SegmentOSD-{}.wav".format(segment)
        self.output_path = os.path.join(OUTPUT_WAV_DIR, self.output_path)
        sf.write(self.output_path, self.audio[int(start*self.sr):int(end*self.sr)], self.sr, 'PCM_24')


#Speaker Change Detection
class SCD:
    def __init__(self, model_path=MODEL_DIR_SCD, model=MODEL_SCD):
        try:
            self.scd = torch.hub.load(model_path, model)
            print("Load SCD Model Sucessfull!")

        except:
            print("Load SCD Model Failed!")

    def process(self, file_path):
        self.file_path = file_path
        self.audio, self.sr = sf.read(self.file_path['audio'])
        self.scd_scores = self.scd(file_path)
        self.peak = Peak(alpha=0.10, min_duration=0.10, log_scale=True)
        self.partition = self.peak.apply(self.scd_scores, dimension=1)
        self.segmentSize = len(self.partition.for_json()['content'])
        self.segmentTime = self.partition.for_json()['content']
    
    def outputWAV_SCD(self, vad):
        self.segmentCrop = self.partition.crop(vad)
        self.segmentSize = len(self.segmentCrop.for_json()['content'])
        self.segmentNew = self.segmentCrop.for_json()['content']
        for i in range(0,self.segmentSize):
            start = self.segmentNew[i]['start']
            end = self.segmentNew[i]['end']
            self.output_path = "SegmentNEW-{}.wav".format(i)
            self.output_path = os.path.join(OUTPUT_WAV_DIR, self.output_path)
            sf.write(self.output_path, self.audio[int(start*self.sr):int(end*self.sr)], self.sr, 'PCM_24')


#Speaker Embedding & Clustering
#on-progress
class EMB:
    def __init__(self, model_path=MODEL_DIR_EMB, model=MODEL_EMB):
        try:
            self.emb = torch.hub.load(model_path, model)
            print("Load SCD Model Sucessfull!")

        except:
            print("Load SCD Model Failed!")

    def check_similarity(self, wav_path_src, wav_path_target):
        self.src_emb = self.emb({'audio:{}'.format(wav_path_src)})
        self.target_emb = self.emb({'audio:{}'.format(wav_path_target)})
        self.distance = cdist(np.mean(self.src_emb, axis=0, keepdims=True), 
                 np.mean(self.target_emb, axis=0, keepdims=True), 
                 metric='cosine')[0, 0]



class DIA:
    def __init__(self, model_path=MODEL_DIR_DIA, model=MODEL_DIA):
        try:
            self.dia = torch.hub.load(model_path, model)
            print("Load DIA Model Sucessfull!")

        except:
            print("Load DIA Model Failed!")

    def process(self, file_path):
        self.file_path = file_path
        self.audio, self.sr = sf.read(self.file_path['audio'])
        self.diarization = self.dia(file_path)
        self.segmentSize = len(self.diarization.for_json()['content'])
        self.segmentContent = self.diarization.for_json()['content']

    
    def outputWAV(self, segment):
        start = self.segmentContent[segment]['segment']['start']
        end = self.segmentContent[segment]['segment']['end']
        label = self.segmentContent[segment]['label']
        self.output_path = "SegmentDIA-{}-{}.wav".format(segment,label)
        self.output_path = os.path.join(OUTPUT_WAV_DIR, self.output_path)
        sf.write(self.output_path, self.audio[int(start*self.sr):int(end*self.sr)], self.sr, 'PCM_24')






