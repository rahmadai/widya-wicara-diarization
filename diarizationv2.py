import sys

sys.path.append('src')
import os
import argparse
import widya.diarization
import widya.utils
from pathlib import Path
import calendar;
import time;
import warnings



PATH_DIR = os.path.dirname(os.path.realpath(__file__))
DEFAULT_AUDIO_DIR = os.path.join(PATH_DIR,'dataset/cs_user_verifikasi_normal.wav')
DEFAULT_OUTPUT_DIR = os.path.join(PATH_DIR,'output')

parser = argparse.ArgumentParser()
parser.add_argument('--audio_path', default=DEFAULT_AUDIO_DIR, type=str)
parser.add_argument('--output_path', default=DEFAULT_OUTPUT_DIR,type=str)
parser.add_argument('--save_audio_segment', default=True)
parser.add_argument('--set_num_speaker', default=2, type=int)

global args
args = parser.parse_args()

def CreateFolder(path):
    dir = path
    check = os.path.isdir(dir)

    if not check:
        os.makedirs(dir)


if __name__ == '__main__':
    warnings.filterwarnings("ignore")
    print("\n\nWidya Speaker Diarization V.1")
    print("Input Audio Path : {}".format(args.audio_path))
    print("Output Path : {}".format(args.output_path))

    print("\nLoad Model ")
    #Voice Activity Detection
    vad = widya.diarization.VAD()

    #Sound Change Detection
    scd = widya.diarization.SCD()

    #Segmentation Audio 
    seg = widya.diarization.Segmentation()

    # #Clustering Audio
    cluster = widya.diarization.Clustering()

    file_name = Path(args.audio_path).name[:-4]
    ts = calendar.timegm(time.gmtime())

    #Create output folder
    output_diarization_dir = os.path.join(args.output_path, '{}_{}'.format(ts, file_name))
    
    CreateFolder(path = output_diarization_dir)

    audio_seg_dir = os.path.join(output_diarization_dir, 'audio_seg')
    CreateFolder(path = audio_seg_dir)

    audio_cluster_dir = os.path.join(output_diarization_dir, 'audio_cluster')
    CreateFolder(path = audio_cluster_dir)

    #JSON Wida Utils

    json_widya = widya.utils.JSON(output_dir = audio_seg_dir)


    #Processing Audio Segmentation

    #Voice Activity Detection Process
    vad.process(args.audio_path)

    #Speaker Change Detection Process
    scd.process(args.audio_path)

    #Segmented Audio Based on VAD and SCD Results
    seg.process(vad, scd)

    ##Save Segmentation Audio Timestamp
    json_widya.CreateJSONAudioSegment(args.audio_path, seg.segmentTime, file_name="audio_segment.json")

    #Create WAV based on Segmentation Audio Timestamp
    wav_out = widya.utils.Audio()
    json_path = os.path.join(audio_seg_dir, 'audio_segment.json')
    wav_out.generateWAVFromJSON(json_path=json_path, output_dir=audio_seg_dir)

    #Speaker Ref
    speaker = widya.utils.Speaker(args.set_num_speaker)
    speaker.setSpeakerName()
    speakerRef = speaker.setSpeakerAudioRef(json_path = os.path.join(audio_seg_dir, 'seg_audio.json'))

    #Clustering Speaker
    cluster.processFromJSON(speakerRef, json_path = os.path.join(audio_seg_dir, 'seg_audio.json'))

    #Padding Audio
    cluster.processPadding(json_cluster_path=os.path.join(audio_seg_dir, 'clustering_audio.json'), output_dir=audio_cluster_dir)

    # #STT Process
    stt = widya.utils.STT(json_file= os.path.join(audio_cluster_dir, 'clustering_segment.json'), output_dir=output_diarization_dir)
    stt.process()




    

