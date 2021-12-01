import widya


# Audio File Path
# test_file = {'uri': 'filename', 'audio': '/home/hamz/speaker-diarization/speaker-diarization/dataset/test/test_1.wav'}
# test2_file = {'uri': 'filename', 'audio': '/home/hamz/speaker-diarization/speaker-diarization/dataset/test/test_2.wav'}
test3_file = {'uri': 'filename', 'audio': '/home/hamz/Part Time/speaker-diarization/dataset/test/Widya-Diarization-003.wav'}


#Voice Activity Detection, Overlap Speech Detection & Speaker Change Detection Declaration
vad = widya.VAD()
osd = widya.OSD()
scd = widya.SCD()

AUDIO_PATH= test3_file

vad.process(AUDIO_PATH)
scd.process(AUDIO_PATH)
osd.process(AUDIO_PATH)


#Function to print all timelines from VAD
print(vad.result)

#Function to print all timelines from SCD
print(scd.partition)

#Function to print all timelines from OSD
print(osd.overlap)

#Function to create WAV files from VAD
for i in range(0, vad.segmentSize):
    vad.outputWAV(segment=i)

#Function to create WAV files from SAD
for i in range(0, scd.segmentSize):
    scd.outputWAV(segment=i)


#Function to create WAV files from OSD
for i in range(0, osd.segmentSize):
    osd.outputWAV(segment=i)


#Function to get segmentation audio based on VAD & SAD
scd.outputWAV_SCD(vad.result)


#Function to print all timelines segmentation audio
print(scd.partition.crop(vad.result))
