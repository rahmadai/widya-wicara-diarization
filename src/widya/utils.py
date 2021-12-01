import soundfile as sf
import os
import shutil
import json
import speech_recognition as sr

class JSON:
    """
    A class used to make JSON file for speaker diarization
    """
    
    def __init__(self, output_dir,):
        self.output_dir = output_dir 
        self.dict = {}

    def CreateJSONAudioSegment(self, audio_path, timeSegment, overlapSegment=None, file_name = "audio_segment.json"):
        self.dict['audio_path'] = audio_path
        self.timeSegmentList = self.timeSegmentDict2List(timeSegment)
        self.dict['time_segment'] = self.timeSegmentList
        

        if(overlapSegment!=None):
            self.dict['overlap_segment'] = overlapSegment

        try:
            self.file_dir = os.path.join(self.output_dir, file_name)
            with open(self.file_dir, 'w') as outputfile:
                json.dump(self.dict, outputfile, indent=1)
            
            print("audio segment json saved in {}".format(self.file_dir))

        except:
            print("your output directory location maybe invalid or no available")
    
    def timeSegmentDict2List(self, dict_data):
        list_data = []
        for index in range(0, len(dict_data)):
            temp = {}
            duration = abs(dict_data[index]['start']-dict_data[index]['end'])
            print(duration)
            if(duration>0.3):
                temp['start'] = dict_data[index]['start']
                temp['end'] = dict_data[index]['end']
                list_data.append(temp)
        return list_data

class Audio:
    def __init__(self):
        pass

    def generateWAV(self, segmentTime, type, audio_path, output_dir):
        self.audio, self.sr = sf.read(audio_path)
        self.output_dir = output_dir
        self.segmentTime = segmentTime
        self.output_dir_new = os.path.join(self.output_dir,type)
        self.segmentSize = len(self.segmentTime)
        for index in range(0, self.segmentSize):
            start = self.segmentTime[index]['start']
            end = self.segmentTime[index]['end']
            print('{} + {}'.format(start, end))
            self.file_name = "seg_audio-{}.wav".format(index)
            self.output_wav_dir = os.path.join(self.output_dir_new,self.file_name)
            sf.write(self.output_wav_dir, self.audio[int(start*self.sr):int(end*self.sr)], self.sr, 'PCM_24')
    
    def generateWAVFromJSON(self, json_path, output_dir):
        self.file_json = open(json_path)
        self.json_data = json.load(self.file_json)
        self.audio, self.sr = sf.read(self.json_data['audio_path'])
        
        # print(self.json_data['time_segment'])
        print("Create WAV Files")
        self.timeSegment = self.json_data['time_segment']
        self.json_out = []
        for index in range(0, len(self.timeSegment)):
            json_wav = {}
            file_name = "seg_audio-{}.wav".format(index)
            start = self.timeSegment[index]['start']
            end = self.timeSegment[index]['end']
            file_out_dir = os.path.join(output_dir, file_name)

            json_wav['file_name'] = file_name
            json_wav['duration'] = abs(start-end)
            timestamp = {'start':start, 'end':end}
            json_wav['timestamp'] = timestamp

            try:
                sf.write(file_out_dir, self.audio[int(start*self.sr):int(end*self.sr)], self.sr, 'PCM_24')
                self.json_out.append(json_wav)
            except:
                print("Fail to generate WAV")
        
        self.json_file_dir = os.path.join(output_dir, 'seg_audio.json')

        with open(self.json_file_dir, 'w') as outputfile:
            try:
                json.dump(self.json_out, outputfile, indent=1)
                print("audio _seg json saved in {}".format(self.json_file_dir))
            except:
                print("Failed to save json file")
        
        

class Speaker:
    def __init__(self, num_speaker):
        self.num_speaker = num_speaker
    
    def setSpeakerName(self):
        self.speakerName = []
        for index in range(0, self.num_speaker):
            print("Masukan Nama Speaker {} = ".format(index))
            self.speakerName.append(input())
        try:
            self.speakerName.index('ilham')
            print("Ada")
        except:
            print("not available")
            
    def setSpeakerAudioRef(self, json_path):
        self.file_json = open(json_path)
        self.json_data = json.load(self.file_json)
        print(len(self.json_data))
        wav_files = []
        duration = []
        for index in range(0, len(self.json_data)):
            wav_files.append(self.json_data[index]['file_name'])
            duration.append(self.json_data[index]['duration'])

        print(wav_files)
        print(duration)

        duration, wav_files = zip(*sorted(zip(duration, wav_files),reverse=True))

        print(wav_files)
        print(duration)

        self.files_list = wav_files
        self.speakerRef = ["" for i in range(0, self.num_speaker)]
        for file in self.files_list:
            if(self.checkAudioRef()==1):
                break

            print("Suara siapa pada file {}".format(file))
            print("Daftar Speaker = {}".format(", ".join(self.speakerName)))
            print("Speaker : ")
            while(1):
                spk = input()
                print("\n")
                try:
                    index_speaker = self.speakerName.index(spk)
                    if(self.speakerRef[index_speaker]==''):
                        self.speakerRef[index_speaker]=file
                    break
                except:
                    print("Nama speaker salah pastikan input sesuai dengan nama yang tersedia!")
                    print("Suara siapa pada file {}".format(file))
                    print("Daftar Speaker = {}".format(", ".join(self.speakerName)))
                    print("Speaker : ")
        dictSpeakerRef = {}
        dictSpeakerRef['name'] = self.speakerName
        dictSpeakerRef['ref_wav'] = self.speakerRef
        return dictSpeakerRef

    def checkAudioRef(self):
        for i in self.speakerRef:
            if(i==''):
                return 0 
        return 1
    

class SpeakerAudioGenerator:
    def __init__(self, output_dir):
        self.input_dir = os.path.join(output_dir,'segmentation')
        self.output_dir = os.path.join(output_dir,'clustering')
    
    def generateWAV(self, speakerDict):
        list_speaker = list(speakerDict.keys())
        for speaker in list_speaker:
            speaker_wav = speakerDict[speaker]
            index = 0
            for wav in speaker_wav:
                original_path = os.path.join(self.input_dir, wav)
                target_path = os.path.join(self.output_dir, '{}-{}.wav'.format(speaker,index))
                original = r'{}'.format(original_path)
                target = r'{}'.format(target_path)
                shutil.copyfile(original, target)
                index+=1

class STT:
    def __init__(self, json_file, output_dir):
        self.json_path = json_file
        self.wav_dir = os.path.dirname(json_file)
        self.output_dir = output_dir
    
    
    def process(self):
        self.file_json = open(self.json_path)
        self.json_data = json.load(self.file_json)
        self.json_out = []

        for index in range(0, len(self.json_data)):
            json_temp = {}

            file_name = self.json_data[index]['file_name']
            wav_path = os.path.join(self.wav_dir, file_name)

            #Translate wav to text using google speech recognition
            r = sr.Recognizer()
            with sr.AudioFile(wav_path) as source:
                audio = r.record(source)
            try:
                # print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
                json_temp['transcript'] = r.recognize_google(audio, language='id')
                # json_temp['transcript'] = r.recognize_google(audio)
            except sr.UnknownValueError:
                json_temp['transcript'] = 'Speech recognition could not understand audio!'
                # print("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                # print("Could not request results from Google Speech Recognition service; {0}".format(e))
                json_temp['transcript'] = 'Speech recognition could not understand audio!'

            json_temp['file_name'] = file_name
            json_temp['speaker'] = self.json_data[index]['speaker']
            json_temp['duration'] = self.json_data[index]['duration']
            json_temp['timestamp'] = self.json_data[index]['timestamp']
            if(json_temp['transcript']!='Speech recognition could not understand audio!'):  
                self.json_out.append(json_temp)

        #Create JSON file 
        self.json_file_dir = os.path.join(self.output_dir, 'diarization.json')
        with open(self.json_file_dir, 'w') as outputfile:
            try:
                json.dump(self.json_out, outputfile, indent=1)
                print("stt_audio json saved in {}".format(self.json_file_dir))
            except:
                print("Failed to save json file")




