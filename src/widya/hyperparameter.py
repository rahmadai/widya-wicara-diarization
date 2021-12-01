
#Widya Diarization Hyperparameter

class Hyperparameter:
    model_dir = 'pyannote/pyannote-audio'
    model_vad_dihard = 'models/Dihard/SAD/sad_dihard/train/X.SpeakerDiarization.DIHARD_Official.train/weights'
    model_osd_dihard = 'models/Dihard/OVL/ovl_dihard/train/X.SpeakerDiarization.DIHARD_Official.train/weights'
    model_scd_dihard = 'models/Dihard/SCD/scd_dihard/train/X.SpeakerDiarization.DIHARD_Official.train/weights'
    model_emb_voxceleb = 'models/Dihard/EMB/emb_voxceleb/train/X.SpeakerDiarization.VoxCeleb.train/weights'
    model_dia = 'dia_ami'
    silence_wav = 'src/widya/silence.wav'
    model_scd_widya = 'models/Widya/SCD/Widya-SCD/weights'
    