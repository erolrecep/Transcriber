<<<<<<< HEAD
# transcriber
A video transcription project to make YouTube videos audio content available as text
=======
# YouTube Transcriber


## Installation

This repository includes couple options for transcription;
 - YouTube video transcriber
 - A video transcriber
 - Record your voice and transcriber afterwards
 - Transcribe while speaking


For each use case's you need to install couple different softwares/libraries.

The main use case is downloading a video / videos (as audio) from YouTube and transcribe them. For this use case, these steps should be followed;

 - clone the repository

 		$ git clone https://github.com/erolrecep/Transcriber.git

 - Install SoX Swiss army knife for audio processing things

 		$ brew install sox      					# For Mac Os X
 		$ sudo apt install sox  					# For Ubuntu

 - create a new Python virtual environment

 		$ conda create --name transcriber python=3.6
 		$ conda activate transcriber
 		$ conda install tensorflow==1.13.1  		# if you have GPU, then install *conda install tensorflow-gpu==1.13.1*  (surprisingly I like this version of tensorflow :) )
 		$ pip install youtube-dl deepspeech==0.7.4  # if you have GPU, then install *pip install deepspeech-gpu==0.7.4*

 - Download pre-trained DeepSpeech models from [here](https://github.com/mozilla/STT/releases/tag/v0.7.4)

 	+ This repository uses 0.7.4 version of the DeepSpeech, you can try the same setup with newer models.
 	+ You need to download [0.7.4 pdmm file](https://github.com/mozilla/DeepSpeech/releases/download/v0.7.4/deepspeech-0.7.4-models.pbmm)
 	+ If you want, you can also download and load scorer provided by Mozilla, [scorer](https://github.com/mozilla/DeepSpeech/releases/download/v0.7.4/deepspeech-0.7.4-models.scorer)

 - Now, the virtual environment is ready, the next step is run the project. For your convenience, I provided a sample .wav file so you can test your setup if it's working. Also, you can download audio files from [here](http://www.voiptroubleshooter.com/open_speech/american.html)

 		$ python run.py --audio audio_files/sample.wav



>>>>>>> b0526b5cdb6482245db3d0424c4ac2f402391ee2
