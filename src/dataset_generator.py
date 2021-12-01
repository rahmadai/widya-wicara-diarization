import sys
import os
from pydub import AudioSegment
import re
import random 

#TTS Path
INPUT_PATH = '/home/hamz/Part Time/STT_Dataset/005/audio'
OUTPUT_ID_NAMES = 'WDY-DZ'

#OUTPUT FOLDER PATH
OUTPUT_PATH = '/home/hamz//Part Time/widya-dataset/speaker-diarization/005'

SIZE_WAV = 200
FIRST_INDEX = 800
SEED_RANDOM = 20
SIZE_SEGMENT_PER_SPEAKER = 5


def printSpeakerSize(speakerDict):
    speakers = list(speakerDict.keys())
    for speaker in speakers:
        print("{} = {} wav files".format(speaker, len(speakerDict[speaker])))

if __name__ == "__main__":
    files = os.listdir(INPUT_PATH)
    
    #Find all speaker
    list_speaker = []
    for file in files:
        regex = r"[a-z0-9]+"
        x = re.findall(regex, file)
        if((x[0] in list_speaker) == False):
            list_speaker.append(x[0])
    
    #Create index files all speaker
    speaker_dict = {}
    for speaker in list_speaker:
        list_wav = []
        for file in files:
            if((speaker in file)==True):
                list_wav.append(file)
        speaker_dict[speaker] = list_wav
    
    print("There are {} speaker in this directory".format(len(speaker_dict)))
    printSpeakerSize(speaker_dict)

    list_rttm = []
    list_uem = []

    #WAV generator
    for index in range(FIRST_INDEX, FIRST_INDEX+SIZE_WAV):
        print('\n')
        y = 0
        timestamp_start = 0
        #Speaker Number & Speaker Ref Generator
        speakerNum = random.randint(2,5)
        speakerRef = []
        for i in range(0, speakerNum):
            speakerIndex = random.randint(0, len(list_speaker)-1)
            while((speakerIndex in speakerRef)==True):
                 speakerIndex = random.randint(0, len(list_speaker)-1)
            speakerRef.append(speakerIndex)

        index_num = f'{index:04}'
        file_name = "{}-{}.wav".format(OUTPUT_ID_NAMES, index_num)
        file_name2 = "{}-{}".format(OUTPUT_ID_NAMES, index_num)
    
        for segment in range(0, SIZE_SEGMENT_PER_SPEAKER):
            for speakerIndex in speakerRef:
                speakerID = list_speaker[speakerIndex]
                sizeSpeakerFiles = len(speaker_dict[speakerID])
                indexFiles = random.randint(0, sizeSpeakerFiles-1)
                wavFilesName = speaker_dict[speakerID][indexFiles]
                inputAudioPath = os.path.join(INPUT_PATH,  wavFilesName)
                x = AudioSegment.from_wav(inputAudioPath)[2000:-2000]
                y+= x
                duration = len(x)/1000.0
                rttm_txt ="SPEAKER {} 1 {} {} <NA> <NA> {} <NA> <NA>".format(file_name2, timestamp_start, duration, speakerID)
                
                list_rttm.append(rttm_txt)
                print(rttm_txt)
                timestamp_start+=duration
        uem_txt = "{} {} {}".format(file_name2, 0.000, timestamp_start)
        print(uem_txt)
        list_uem.append(uem_txt)

        outputAudioPath = os.path.join(OUTPUT_PATH, file_name)
        print(outputAudioPath)
        y.export(outputAudioPath, format ='wav')
    
    #Create UEM & RTTM Files
    rttm_path = os.path.join(OUTPUT_PATH, "WDY-DZ.train.rttm")
    with open(rttm_path, 'w') as file:
        for rttm in list_rttm:
            file.writelines(rttm)
            file.writelines('\n')
    
    uem_path = os.path.join(OUTPUT_PATH, "WDY-DZ.train.uem")
    with open(uem_path, 'w') as file:
        for uem in list_uem:
            file.writelines(uem)
            file.writelines('\n')

        
            

        

    