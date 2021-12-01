

<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/rahmadai/widya-wicara-diarization">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">Widya Wicara Speaker Diarization</h3>

  <p align="center">
    Audio to Text Automation Transciption
    <br />
<!--     <a href="https://github.com/rahmadai/widya-wicara-diarization"><strong>Explore the docs »</strong></a> -->
    <br />
    <br />
    <!-- ·
    <a href="https://github.com/rahmadai/widya-wicara-diarization">Report Bug</a>
    ·
    <a href="https://github.com/rahmadai/widya-wicara-diarization">Request Feature</a> -->
  </p>
</p>

<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

Use miniconda to isolated the environment
* <a href="https://conda.io/projects/conda/en/latest/user-guide/install/index.html#regular-installation">Install Miniconda</a>
* Create new environment with python 3.7.5
  ```sh
  conda create --name diarization python=3.7.5
  ```
  
* Activate the new environment 
  ```sh
  conda activate diarization
  ```
### Installation
 1. Clone repo
  ```sh
  git clone https://username:password@github.com/rahmadai/widya-wicara-diarization.git
  ```
 2. Install package & depedencies
  ```sh
  cd widya-wicara-diarization
  pip install -r requirements.txt 
  ```


  
## Usage
  Audio file recommended format
  <br />
  Frequency : 16000Hz
  <br />
  Format : PCM16
  ```sh
  python diarizationv2.py --audio_path=path/to/your/audio/file.wav --output_path=path/output --set_num_speaker=2
  ```

<!-- LICENSE -->
## License
Copyright (C) Widya Wicara, Inc - All Rights Reserved </br>
For internal use only </br>
Written by Rahmad Kurniawan & Ilham Fazri, 2021

<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements
* [Pyannnote Audio](https://github.com/pyannote/pyannote-audio)
* [SpeechRecognition](https://github.com/Uberi/speech_recognition)
* [Pydub](https://github.com/jiaaro/pydub)

