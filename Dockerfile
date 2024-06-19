FROM python:3.12.2-slim
WORKDIR /app

# create the whisper model cache directory
RUN mkdir -p ~/.cache/whisper

# copy the pre-downloaded Whisper model files from the build context
COPY whisper_models/ ~/.cache/whisper

# install ffmpeg
RUN apt-get update && apt-get install -y ffmpeg

# install dependencies
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# copy application code
COPY . /app/

CMD ["python", "main.py"]
