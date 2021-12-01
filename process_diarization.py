import sys

sys.path.append('src')
import os
import argparse
import widya.diarization
import widya.utils

PATH_DIR = os.path.dirname(os.path.realpath(__file__))
DEFAULT_AUDIO_DIR = os.path.join(PATH_DIR,'dataset/Widya-Diarization-003.wav')
DEFAULT_OUTPUT_DIR = os.path.join(PATH_DIR,'output')

#Parser
parser = argparse.ArgumentParser()
parser.add_argument('--audio_path', default=DEFAULT_AUDIO_DIR, type=str)
parser.add_argument('--output_path', default=DEFAULT_OUTPUT_DIR,type=str)

global args
args = parser.parse_args()


if __name__ == '__main__':
    # #Voice Activity Detection
    vad = widya.diarization.VAD()

    #Sound Change Detection

    #use parameter model='scd_widya' if want to use our model
    scd = widya.diarization.SCD()

    #Segmentation Audio 
    seg = widya.diarization.Segmentation()

    # #Clustering Audio
    cluster = widya.diarization.Clustering()

    #JSON Wida Utils
    json_widya = widya.utils.JSON('/home/hamz/Part Time/widya-wicara-diarization/out_seg')
    
    #Processing Audio Segmentation

    #Voice Activity Detection Process
    vad.process(args.audio_path)

    #Speaker Change Detection Process
    scd.process(args.audio_path)

    #Segmented Audio Based on VAD and SCD Results
    seg.process(vad, scd)

    ##Save Segmentation Audio Timestamp
    json_widya.CreateJSONAudioSegment(DEFAULT_AUDIO_DIR, seg.segmentTime, file_name="audio_segment.json")

    # #Create WAV based on Segmentation Audio Timestamp
    wav_out = widya.utils.Audio()
    json_path = '/home/hamz/Part Time/widya-wicara-diarization/out_seg/audio_segment.json'
    out_dir = '/home/hamz/Part Time/widya-wicara-diarization/out_seg'
    wav_out.generateWAVFromJSON(json_path=json_path, output_dir=out_dir)

    speaker = widya.utils.Speaker(2)
    speaker.setSpeakerName()
    speakerRef = speaker.setSpeakerAudioRef('/home/hamz/Part Time/widya-wicara-diarization/out_seg/seg_audio.json')
    
    cluster.processFromJSON(speakerRef, '/home/hamz/Part Time/widya-wicara-diarization/out_seg/seg_audio.json')
    
    cluster.processPadding('/home/hamz/Part Time/widya-wicara-diarization/out_seg/clustering_audio.json')
    # #STT Process
    stt = widya.utils.STT('/home/hamz/Part Time/widya-wicara-diarization/out_seg/padding/clustering_segment.json')
    stt.process()