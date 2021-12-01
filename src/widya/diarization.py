import torch
import os
import soundfile as sf
import numpy as np
from pyannote.audio.utils.signal import Binarize
from pyannote.audio.utils.signal import Peak
from scipy.spatial.distance import cdist
from widya.hyperparameter import Hyperparameter as hp
from pydub import AudioSegment
from pyannote.audio.features import Pretrained

import json
import numpy

from widya.utils import Audio

class VAD:
    def __init__(self, model=hp.model_vad_dihard):     
        try:
            self.sad = Pretrained(validate_dir = model)
            print("Load VAD Model Sucessfull!")

        except:
            print("Load VAD Model Failed!")

    def process(self, file_path):
        self.file_path = {'uri':'filename','audio':'{}'.format(file_path)}
        self.sad_scores = self.sad(self.file_path)
        self.binarize = Binarize(offset=0.52, onset=0.52, log_scale=True, 
                    min_duration_off=0.1, min_duration_on=0.1)
        self.result = self.binarize.apply(self.sad_scores, dimension=1)
        self.segmentSize = len(self.result.for_json()['content'])
        self.segmentTime = self.result.for_json()['content']

class SCD:
    def __init__(self, model=hp.model_scd_dihard):
        # try:
        if(model == 'scd_widya'):
            self.scd = Pretrained(validate_dir=hp.model_scd_widya)
            print("Load VAD Model Sucessfull!")

        else:
            self.scd = Pretrained(validate_dir=model)
            print("Load SCD Model Sucessfull!")

        # except:
        #     print("Load SCD Model Failed!")

    def process(self, file_path):
        self.file_path = {'uri':'filename','audio':'{}'.format(file_path)}
        self.scd_scores = self.scd(self.file_path)
        self.peak = Peak(alpha=0.50, min_duration=1.0, log_scale=True)
        self.partition = self.peak.apply(self.scd_scores, dimension=1)
        self.segmentSize = len(self.partition.for_json()['content'])
        self.segmentTime = self.partition.for_json()['content']

class Segmentation:
    def __init__(self):
        pass
    def process(self, VAD, SCD):
        self.VAD = VAD
        self.SCD = SCD
        self.segmentCrop = self.SCD.partition.crop(self.VAD.result)
        self.segmentSize = len(self.segmentCrop.for_json()['content'])
        self.segmentTime = self.segmentCrop.for_json()['content']

class Clustering:
    def __init__(self, model = hp.model_emb_voxceleb):
        # try:
            self.emb = Pretrained(validate_dir = model)
            print("Load EMB Model Sucessfull!")

        # except:
        #     print("Load EMB Model Failed!")
    
    def process(self, speakerAudioRef, speakerName, output_dir):
        self.output_dir = os.path.join(output_dir,'segmentation')
        self.speakerName = speakerName
        self.speakerAudioRef = []

        for audioRef in speakerAudioRef:
            path = os.path.join(self.output_dir,audioRef)
            self.speakerAudioRef.append({'audio': '{}'.format(path)})

        self.files_list = os.listdir(self.output_dir)
        self.audioSpeaker = []
        for speaker in range(0, len(self.speakerName)):
            tmp = []
            self.audioSpeaker.append(tmp)

        for file in self.files_list:
            target_file = os.path.join(output_dir,'segmentation')
            target_file = os.path.join(target_file,file)
            target_path = {'audio': '{}'.format(target_file)}

            self.target_emb = self.emb(target_path)
            self.similarityValue = []
            for i in range(0, len(self.speakerName)):
                self.ref_emb = self.emb(self.speakerAudioRef[i])
                distance = cdist(np.mean(self.ref_emb, axis=0, keepdims=True), 
                np.mean(self.target_emb, axis=0, keepdims=True), 
                metric='cosine')[0, 0]
                self.similarityValue.append(distance)
            
            min_index = self.similarityValue.index(min(self.similarityValue))
            tmp_list = self.audioSpeaker[min_index]
            tmp_list.append(file)
            self.audioSpeaker[min_index] = tmp_list
        self.dict_speaker = {}

        for i in range(0,len(self.speakerName)):
            self.dict_speaker[self.speakerName[i]] = self.audioSpeaker[i]
        
        print(self.dict_speaker)
    
    def processPadding(self, json_cluster_path,  output_dir, silence=False):
        self.file_json = open(json_cluster_path)
        self.json_data = json.load(self.file_json)
        self.dirname = os.path.dirname(json_cluster_path)
        self.file_dir_out = output_dir

        self.silence_wav = AudioSegment.from_wav(hp.silence_wav)
        lastSpeaker = ''
        index_out = 0
        json_out = []
        json_temp = {}
        timestamp_temp = {}
        for index in range(0, len(self.json_data)):
            speakerName = self.json_data[index]['speaker']
            file_wav_dir = os.path.join(self.dirname, self.json_data[index]['file_name'])
            print(file_wav_dir)
            if(speakerName!=lastSpeaker):
                if(index!=0):
                    json_temp = {}
                    file_wav_out = os.path.join(self.file_dir_out,'segment-{}.wav'.format(index_out))
                    json_temp['file_name'] = 'segment-{}.wav'.format(index_out)
                    json_temp['speaker'] = lastSpeaker
                    json_temp['duration'] = abs(timestamp_temp['start']-timestamp_temp['end'])
                    json_temp['timestamp'] = timestamp_temp
                    json_out.append(json_temp)
                    index_out+=1
                    y.export(file_wav_out, format ='wav')
                lastSpeaker = speakerName
                timestamp_temp['start'] =  self.json_data[index]['timestamp']['start']
                timestamp_temp['end'] = self.json_data[index]['timestamp']['start']
                y = AudioSegment.from_wav(file_wav_dir)
                

            else:
                x = AudioSegment.from_wav(file_wav_dir)
                silence_duration = self.json_data[index]['timestamp']['start']-self.json_data[index-1]['timestamp']['end']
                timestamp_temp['end'] = self.json_data[index]['timestamp']['end']
                if(silence==True): 
                    y+=self.silence_wav[0:int(silence_duration*1000)]
                y+=x

            if(index==len(self.json_data)-1):
                file_wav_out = os.path.join(self.file_dir_out,'segment-{}.wav'.format(index_out))
                y.export(file_wav_out, format ='wav')

        self.json_file_dir = os.path.join(self.file_dir_out,'clustering_segment.json')
        print(json_out)
        with open(self.json_file_dir, 'w') as outputfile:
            try:
                json.dump(json_out, outputfile, indent=1)
                print("clutering _seg json saved in {}".format(self.json_file_dir))
            except:
                print("Failed to save json file")
            
                

    def processFromJSON(self, speakerRef, json_path):
        self.speakerName = speakerRef['name']
        self.speakerRef = speakerRef['ref_wav']
        self.audio_dir = os.path.dirname(json_path)

        self.file_json = open(json_path)
        self.json_data = json.load(self.file_json)

        self.speaker_emb = []
        for wav_dir in self.speakerRef:
            wav_file = os.path.join(self.audio_dir,wav_dir)
            speaker_path = {'audio': '{}'.format(wav_file)}
            emb = self.emb(speaker_path)
            self.speaker_emb.append(emb)
            
        json_out = []
        for index in range(0, len(self.json_data)):
            target_path = os.path.join(self.audio_dir,self.json_data[index]["file_name"])
            target_file = {'audio': '{}'.format(target_path)}
            print(target_file)
            target_emb = self.emb(target_file)
            distance_value = []
            for index_speaker in range(0, len(self.speaker_emb)):
                distance = cdist(np.mean(target_emb, axis=0, keepdims=True), 
                    np.mean(self.speaker_emb[index_speaker], axis=0, keepdims=True), 
                    metric='cosine')[0, 0]
                distance_value.append(distance)
            
            json_wav = {}
            json_wav['file_name'] = self.json_data[index]['file_name']
            json_wav['speaker'] = self.speakerName[distance_value.index(min(distance_value))]
            json_wav['duration'] = self.json_data[index]['duration']
            json_wav['timestamp'] = self.json_data[index]['timestamp']
            json_out.append(json_wav)

        
        self.json_file_dir = os.path.join(self.audio_dir, 'clustering_audio.json')

        with open(self.json_file_dir, 'w') as outputfile:
            try:
                json.dump(json_out, outputfile, indent=1)
                print("clutering _seg json saved in {}".format(self.json_file_dir))
            except:
                print("Failed to save json file")
        



        
        
