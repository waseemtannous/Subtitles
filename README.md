# Subtitles

The aim of this project is to build a pipeline for processing a video (recorded lecture), use speech recognition and machine translation libraries to generate subtitles from Hebrew to English and Arabic. The pipeline will include the following steps:

- Extract audio from video.
- Transcribe audio to text.
- Translate text from Hebrew (or any language) to English and Arabic.
- Generate subtitles and add them to the video.

## Project Description (from moodle)

Speech recognition and machine translation technologies have developed so much in recent years that it is now possible to convert speech to text, in a variety of languages, with very high accuracy, and to translate this text to a variety of languages, again with high faithfulness to the source language and fluency in the target language. The goal of this project is to develop a pipeline that uses available tools for speech recognition and machine translation and automatically adds subtitles to online courses.

The project will focus one specific course, Introduction to Computer Science, and three languages: Hebrew (the original speech language), Arabic, and English (two target languages). However, the idea is to develop a fully-automated pipeline that, given a set of videos, will be able to generate subtitles in any language (either the original one or a translated one) and attache them to the video. The pipeline will then be tested on another course, Natural Language Processing.

## Tech Stack and Libraries

`python` is used to write the code. The following libraries and dependencies are used in the project:

- `moviepy` for video editing and audio extraction.
- `whisper` for speech recognition.
- `deep_translator` for machine translation. Specifically, the code uses Google Translate API.
- `python-dotenv` for environment variables.
- `ffmpeg` for video editing and burning subtitles to video.

`.srt` is a widely used file format for subtitles.

## Whisper

Whisper is a speech recognition library by OpenAI. It transcribes audio to text. It has multiple models with different sizes and accuracies.

You can find available models, sizes, and required resouces [here](https://github.com/openai/whisper?tab=readme-ov-file#available-models-and-languages).

For this project, I used the biggest one, `large`, to get the highest accuracy. It requires 10GB of vRAM to run. Use a smaller model if you have limited resources and vRAM.

When whisper runs for the first time, it downloads the specified model. It takes some time to download the model. The model is saved in the `~/.cache/whisper` directory.

For easier use and to avoid downloading the model every time, I pre-downloaded the models and included them in the [Google Drive folder](https://drive.google.com/drive/folders/1lD2icryVlPvtFsM-mRilJysx7qpLR-HH). You can find the models in the `whisper_models` directory. Download the directory and place it in the project root.

## Installation and Running the Pipeline

Install `python3` and `ffmpeg` on your machine and clone the repo (skip this step if you already have python and ffmpeg installed):

```bash
sudo apt update
sudo apt install python3 python3-pip
sudo apt install ffmpeg
git clone https://github.com/waseemtannous/Subtitles.git
```

Create a `data` directory in the project root.

Populate this directory with 2 directories:

- `videos`: Put the video you want to process in this directory.
- `output`: empty directory to store the output videos and subtitles.

An example directory is found in the [Google Drive folder](https://drive.google.com/drive/folders/1lD2icryVlPvtFsM-mRilJysx7qpLR-HH) named `data`. Download it and place it in the project root. It contains sample videos to test the pipeline.

Double check the `.env` file and make sure the right environment variables are set. Example:

```bash
VIDEOS_PATH = 'data/videos'
OUTPUT_PATH = 'data/output'

# True - if you want to translate the subtitles to other languages
TRANSLATE = "True"
# TRANSLATE = "False"

#en - English
#ar - Arabic
#iw - Hebrew (if the original language is hebrew, no need to use it in the target languages)
# you can add more languages separated by comma
# if TRANSLATE is False, this variable will be ignored
LANGUAGE_CODES = 'en,ar'

# True - if you want also create a subtitles video with the original language
ORIGINAL_SUBTITLES = "True"
# ORIGINAL_SUBTITLES = "False"

# WHISPER_MODEL_SIZE = 'tiny'
# WHISPER_MODEL_SIZE = 'base'
# WHISPER_MODEL_SIZE = 'small'
# WHISPER_MODEL_SIZE = 'medium'
WHISPER_MODEL_SIZE = 'large-v3'
```

Install the python packages and run the pipeline:

```bash
cd Subtitles
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
python3 main.py
```

The pipeline will process all the videos in the `data/videos` directory. It will extract the audio, transcribe it to text, translate the text to all target languages, and generate subtitles. It will also create a video with the subtitles burned in.

## Note

The pipeline is tested on Ubuntu 20.04. It should work on other Linux distributions. It might work on Windows and MacOS, but it is not tested. Also, `python 3.10.12` is used in the project.

The Script is also aware of RTL languages and will flip the subtitles if the language is RTL to make it more readable.

To get the best results, use video with clear audio and no background noise. Also, using the largest whisper model will give the best results but requires 10GB of vRAM. Use a smaller model if you have limited resources. Beware, the large model is slow and might take a long time to process the video but yields the most accuracy.

FFMPEG is used to burn the subtitles to the video. Burnin subtitles to the video might take some time. The video is processed frame by frame to add the subtitles. The process is slow and might take a long time for long videos and it is bound by the machines available resources.

If you want to monitor the usage of the GPU, run the command `watch -n0.1 nvidia-smi` in a separate terminal.
