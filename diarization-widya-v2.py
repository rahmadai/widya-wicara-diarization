file_path = "dataset/cs_user_verifikasi_normal.wav"

import matplotlib.pyplot as plt
HYPER_PARAMETERS = {
  # onset/offset activation thresholds
  "onset": 0.5, "offset": 0.5,
  # remove speech regions shorter than that many seconds.
  "min_duration_on": 0.0,
  # fill non-speech regions shorter than that many seconds.
  "min_duration_off": 0.0
}

from pyannote.audio import Inference
inference = Inference("pyannote/segmentation")
segmentation = inference(file_path)
print(segmentation.data)
# plt.plot(segmentation.data[0].shape)