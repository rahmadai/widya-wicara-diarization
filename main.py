import sys

sys.path.append('src')
import os
import argparse
import widya.diarization
import widya.utils

PATH_DIR = os.path.dirname(os.path.realpath(__file__))
DEFAULT_AUDIO_DIR = os.path.join(PATH_DIR,'dataset/podcast.wav')
DEFAULT_OUTPUT_DIR = os.path.join(PATH_DIR,'output')

#Parser
parser = argparse.ArgumentParser()
parser.add_argument('--audio_path', default=DEFAULT_AUDIO_DIR, type=str)
parser.add_argument('--output_path', default=DEFAULT_OUTPUT_DIR,type=str)

global args
args = parser.parse_args()


if __name__ == '__main__':

    #Voice Activity Detection
    vad = widya.diarization.VAD()

    #Sound Change Detection
    scd = widya.diarization.SCD()

    #Segmentation Audio 
    seg = widya.diarization.Segmentation()

    #Clustering Audio
    cluster = widya.diarization.Clustering()
    

    speaker = widya.utils.Speaker(num_speaker = 2, output_dir = args.output_path)

    output_speaker = widya.utils.SpeakerAudioGenerator(args.output_path)
    output_utils = widya.utils.Audio(args.audio_path, args.output_path)


    vad.process(args.audio_path)
    scd.process(args.audio_path)
    seg.process(vad, scd)
    print(seg.segmentTime)

    
    # output_utils.generateWAV(vad.segmentTime, type = 'segmentation')
    # speaker.setSpeakerName()
    # speaker.setSpeakerAudioRef()
    # cluster.process(speaker.speakerRef, speaker.speakerName, output_dir = args.output_path)

    # output_speaker.generateWAV(cluster.dict_speaker)


