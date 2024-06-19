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
- `ffmpeg` for video editing and burning subtitles to video.
- `docker` for running the pipeline in a containerized environment with all dependencies.

## Whisper

Whisper is a speech recognition library by OpenAI. It transcribes audio to text. It has multiple models with different sizes and accuracies.

You can find available models and sizes [here](https://github.com/openai/whisper?tab=readme-ov-file#available-models-and-languages).

For this project, I used the biggest one, `large`, to get the highest accuracy. It requires 10GB of vRAM to run. Use a smaller model if you have limited resources and vRAM.

When whisper runs for the first time, it downloads the specified model. It takes some time to download the model. For easier use and faster development, The docker image has all the models pre-downloaded. They can also be found in the `whisper_models` directory.

## Build and Run

The project contains a `Dockerfile` that you can use to build a container image and run the pipeline in a containerized environment. The `Dockerfile` installs all dependencies and libraries required to run the pipeline.

To build the image, run the following command:

```bash
docker build -t subtitles .
```

Create a `data` directory in the project root and place the video you want to process in it. Docker will mount this directory to the container.

A docker-compose file is also provided to run the pipeline. To run the pipeline, use the following command:

```bash
docker-compose up
```

The pipeline will process the video named `video.mp4` found in the `data` directory and generate subtitles according to the target language provided as an environment variable in the docker-compose file. The subtitles will be added to the video. The output video will be saved in the `output` directory alongside the `subtitles.srt` file.

`.srt` is a widely used format for subtitles.
