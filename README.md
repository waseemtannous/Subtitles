# Subtitles

## Project Overview

This project aims to automate the process of transcribing videos (mainly in Hebrew), translating the transcriptions into multiple languages, and adding subtitles to the videos. The main objective is to make video content accessible to a broader audience by providing subtitles in various languages. The pipeline will include the following steps:

- Extract audio from video.
- Transcribe audio to text.
- Translate text from Hebrew (or any language) to English and Arabic.
- Generate subtitles and add them to the video.

## Project Description (from moodle)

Speech recognition and machine translation technologies have developed so much in recent years that it is now possible to convert speech to text, in a variety of languages, with very high accuracy, and to translate this text to a variety of languages, again with high faithfulness to the source language and fluency in the target language. The goal of this project is to develop a pipeline that uses available tools for speech recognition and machine translation and automatically adds subtitles to online courses.

The project will focus on one specific course, Introduction to Computer Science, and three languages: Hebrew (the original speech language), Arabic, and English (two target languages). However, the idea is to develop a fully-automated pipeline that, given a set of videos, will be able to generate subtitles in any language (either the original or a translated one) and attaches them to the video.

## Tech Stack and Libraries

`python` is used to write the code. The following libraries and dependencies are used in the project:

- `moviepy` for video editing and audio extraction.
- `whisper` for speech recognition.
- `deep_translator` for machine translation. Specifically, the code uses Google Translate API.
- `python-dotenv` for environment variables.
- `ffmpeg` and `ffmpeg-python` for video editing and burning subtitles to video.

`.srt` is a widely used file format for subtitles.

## Design and Implementation

### Transcription

The transcription is performed using the Whisper model, loaded offline to the GPU, and used to transcribe the audio from the video files. It outputs sentences and the timing for each sentence.

### Translation

The transcribed text is translated into the specified languages using the Google Translate API.

### Subtitles

Subtitles are created and added to the video using FFMPEG. The subtitles are formatted correctly for right-to-left languages like Hebrew and Arabic to ensure proper display.

### Workflow

1. **Transcribe**: Extract audio from the video and transcribe it.
2. **Translate**: Translate the transcribed text into multiple target languages.
3. **Subtitles**: Generate subtitle files and overlay them onto the video using ffmpeg.

## Whisper

Whisper is a speech recognition library by OpenAI that transcribes audio to text. It has multiple models of different sizes and accuracy.

You can find available models, sizes, and required resources [here](https://github.com/openai/whisper?tab=readme-ov-file#available-models-and-languages).

This project uses the biggest `large` model to achieve the highest accuracy. It requires 10GB of vRAM to run. If you have limited resources and vRAM, use a smaller model. The accuracy will be lower, but it will run faster.

When whisper runs for the first time, it downloads the specified model. It takes some time to download the model. The model is saved in the `~/.cache/whisper` directory.

For easier use and to avoid downloading the model every time, I pre-downloaded the models and included them in the [Google Drive folder](https://drive.google.com/drive/folders/1lD2icryVlPvtFsM-mRilJysx7qpLR-HH). You can find the models in the `whisper_models` directory. Download the directory and place it in the project root.

## Experiments and Features

- **Single Language Processing**: The script's first version supported only one target language at a time.

- **Multiple Language Support**: Enhanced the script to handle multiple target languages for each video.

- **Multiple Videos Support**: Improved the pipeline to process multiple videos in a batch.

- **SRT File Type**: This format is the most widely used for subtitles. It is simple and easy to work with. The script generates an SRT file for each language, enabling the user to easily upload the subtitles to video platforms without needing to burn them to the video.

- **Burned Subtitles**: The script also generates a video with the subtitles burned in. This is useful for platforms that do not support SRT files.

- **Right-to-Left Languages**: The script is aware of right-to-left languages like Hebrew and Arabic. It formats the subtitles correctly to ensure proper display.

- **Translation Support**: The script supports translation to multiple languages. The user can specify the target languages in the `.env` file.

- **Model Size**: The script supports different whisper model sizes. The user can specify the model size in the `.env` file.

- **Modular Design**: The script is modular and easy to extend. Everything is wrapped in self-contained functions that can be easily imported and used in other projects. The workflow can be easily changed according to the users' needs.

- **Dynamic Environment Variables**: The script uses environment variables to configure the pipeline. The user can easily change the settings by modifying the `.env` file, making the script flexible and easy to use.

## Alternative Approaches

### Transcription Models

- **Other Transcription Models**: I experimented with various transcription models, but Whisper provided the best accuracy and integration ease. It's an offline model that does not require an internet connection.

- **Online Transcription Services**: Google Cloud Speech-to-Text and Microsoft Azure Speech-to-Text are popular online services. They also provide high accuracy, but there is a cost associated with using them.

### Translation Services

- **Other Translation APIs**: Microsoft Azure Translator Text API and Amazon Translate are other popular translation services. They provide similar functionality, but they are paid services.

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

- `data/videos`: Put the video you want to process in this directory.
- `data/output`: empty directory to store the output videos and subtitles.

An example directory `data` is found in the [Google Drive folder](https://drive.google.com/drive/folders/1lD2icryVlPvtFsM-mRilJysx7qpLR-HH) named `data`. Download it and place it in the project root. It contains short sample videos to test the pipeline.

Review the `.env` file and make sure the right environment variables are set. Example:

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

Install the python packages in a seperate and clean environment and run the pipeline:

```bash
cd Subtitles
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
python3 main.py
```

The pipeline will process all the videos in the `data/videos` directory. It will extract the audio, transcribe it to text, translate the text to all target languages, and generate subtitles. It will also create a video with the subtitles burned in. The output will be saved in the `data/output` an it contains the video with captions, raw audio file, and the srt files for each language.

## Notes

- The pipeline is tested on Ubuntu 20.04. It should work on other Linux distributions. It might work on Windows and MacOS, but it is not tested. `Python 3.10.12` was also used in the project.

- The Script is also aware of RTL languages and will flip the subtitles if the language is RTL to make it more readable.

- To get the best results, use video with clear audio and no background noise. Also, using the largest whisper model will give the best results but requires 10GB of vRAM. Use a smaller model if you have limited resources. Beware: The large model is slower and takes longer to process the video but yields the highest accuracy.

- FFMPEG is used to burn the subtitles to the video. Burnin subtitles to the video might take some time. The video is processed frame by frame to add the subtitles. The speed of the process depends on the video length, resolution, and frame rate.

- To monitor the GPU's usage, run the command `watch -n0.1 nvidia-smi` in a separate terminal.

- The whisper model works best when the audio is clear. It might struggle with noisy audio or multiple speakers. Clean audio is recommended for best results.

- The whisper model yields good accuracy for text, punctuation, and timing. It is trained on a large dataset and can handle various accents and languages. Keep in mind that these models are not perfect and might make mistakes. During the testing, it missed only a few words in a 16-minute video.

## Benchmarks

### Hardware

- CPU: 12th Gen Intel® Core™ i7-12700F
- RAM: 16GB
- GPU: NVIDIA GeForce RTX 3060
- vRAM: 12GB
- OS: Ubuntu 20.04

### Performance

Average runtime for a 16-minute video running at 720p and 60fps using Whisper's largest model:

- Audio extraction: `3 seconds`
- Transcription (offline): `3:20 minutes`
- Translation (1 language - online): `1:30 minutes`
- Subtitles burning (1 srt file): `1:40 minutes`

The total runtime for the same video in Hebrew translated to Arabic and English, and burned subtitles for the three languages is `13 minutes`.
