import torch
from pyannote.audio.utils.signal import Peak
# scd = torch.load('/home/hamz/Part Time/widya-wicara-diarization/models/Widya/SCD/train/WIDYA.SpeakerDiarization.Dataset.train/weights/0005.pt', map_location=torch.device('cpu') )
file_path = {'uri':'filename','audio':'/home/hamz/Part Time/widya-wicara-diarization/dataset/podcast.wav'}
# scd = torch.hub.load('pyannote/pyannote-audio','scd_dihard')
# print(scd)

from pyannote.audio.features import Pretrained
scd = Pretrained(validate_dir='models/Widya/SCD/Widya-SCD/weights')
scd(file_path)
scd_scores = scd(file_path)
peak = Peak(alpha=0.10, min_duration=0.10, log_scale=True)
partition = peak.apply(scd_scores, dimension=1)
segmentSize = len(partition.for_json()['content'])
segmentTime = partition.for_json()['content']
print(segmentTime)