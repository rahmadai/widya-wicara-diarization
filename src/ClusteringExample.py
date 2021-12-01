import torch
model = torch.hub.load('pyannote/pyannote-audio', 'emb')

print(f'Embedding has dimension {model.dimension:d}.')

import numpy as np
from pyannote.core import Segment

speaker1 = model({'audio': '/home/hamz/speaker-diarization/env/tmp/ujicoba/cs.wav'})
speaker2 = model({'audio': '/home/hamz/speaker-diarization/env/tmp/ujicoba/user.wav'})

target = model({'audio': '/home/hamz/speaker-diarization/env/tmp/SegmentNEW-1.wav'})

# Compare speaker embedding
from scipy.spatial.distance import cdist

distance = cdist(np.mean(speaker1, axis=0, keepdims=True), 
                 np.mean(target, axis=0, keepdims=True), 
                 metric='cosine')[0, 0]

print(distance)

distance = cdist(np.mean(speaker2, axis=0, keepdims=True), 
                 np.mean(target, axis=0, keepdims=True), 
                 metric='cosine')[0, 0]

print(distance)