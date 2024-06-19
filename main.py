import whisper
from moviepy.editor import *
from deep_translator import GoogleTranslator
import logging
from time import time

# load the environment variables
VIDEO_PATH = os.environ['VIDEO_PATH']
AUDIO_PATH = os.environ['AUDIO_PATH']
SRT_PATH = os.environ['SRT_PATH']
FINAL_OUTPUT_PATH = os.environ['FINAL_OUTPUT_PATH']
TARGET_LANGUAGE = os.environ['TARGET_LANGUAGE']
WHISPER_MODEL_SIZE = os.environ['WHISPER_MODEL_SIZE']
TRANSLATE = os.environ['TRANSLATE'] == 'True'

# extracts the audio from a video file and saves it to the specified path.
def extract_audio_from_video(video_path, audio_path):
    video_clip = VideoFileClip(video_path)
    audio_clip = video_clip.audio

    # check if a file exists with the same name as the audio_path and delete it if it does
    if os.path.exists(audio_path):
        os.remove(audio_path)
    audio_clip.write_audiofile(audio_path)

    # close the clips to release their resources
    audio_clip.close()
    video_clip.close()

# converts time in seconds to the SRT time format 'HH:MM:SS,ms'
def format_srt_time(seconds):
    milliseconds = int((seconds % 1) * 1000)
    seconds = int(seconds)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"

# save as srt file
def save_as_srt(segments, file_name):
    # check if a file exists with the same name as the file_name and delete it if it does
    if os.path.exists(file_name):
        os.remove(file_name)

    with open(file_name, "w") as file:
        for i, segment in enumerate(segments):
            start_time = format_srt_time(segment['start'])
            end_time = format_srt_time(segment['end'])
            text = segment['text']
            file.write(f'{i + 1}\n')
            file.write(f'{start_time} --> {end_time}\n')
            file.write(f'{text}\n\n')

def create_subtitles_video(video_path, audio_path, srt_path, output_path):
    # remove the output file if it already exists
    if os.path.exists(output_path):
        os.remove(output_path)

    temp_file_path = 'temp_output.mp4'

    # add subtitles to video
    os.system(f'ffmpeg -i {video_path} -vf "subtitles={srt_path}:force_style=\'Fontsize=20\'" -c:a copy {temp_file_path}')

    # add the audio back to the video
    os.system(f'ffmpeg -i {temp_file_path} -i {audio_path} -c:v copy -c:a aac -b:a 192k {output_path}')

    # remove the temporary video file
    if os.path.exists(temp_file_path):
        os.remove(temp_file_path)

    # remove the audio file
    if os.path.exists(audio_path):
        os.remove(audio_path)


def transcribe(audio_path, whisper_model_size):
    model = whisper.load_model(whisper_model_size)
    result = model.transcribe(audio_path, fp16=False)
    return result['segments']

def translate(segments, target_language):
    for segment in segments:
        segment['text'] = GoogleTranslator(source='auto', target=target_language).translate(segment['text'])
    return segments

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    start_time = time()
    logging.info('Extracting audio from video...')
    extract_audio_from_video(VIDEO_PATH, AUDIO_PATH)
    logging.info(f'Audio extracted in {time() - start_time} seconds')

    start_time = time()
    logging.info('Transcribing audio...')
    segments = transcribe(AUDIO_PATH, WHISPER_MODEL_SIZE)
    save_as_srt(segments, 'data/hebrew.srt')
    logging.info(f'Audio transcribed in {time() - start_time} seconds')

    if TRANSLATE:
        start_time = time()
        logging.info('Translating segments...')
        segments = translate(segments, TARGET_LANGUAGE)
        logging.info(f'Segments translated in {time() - start_time} seconds')

    start_time = time()
    logging.info('Saving segments as SRT...')
    save_as_srt(segments, SRT_PATH)
    logging.info(f'Segments saved as SRT in {time() - start_time} seconds')

    start_time = time()
    logging.info('Creating subtitles video...')
    create_subtitles_video(VIDEO_PATH, AUDIO_PATH, SRT_PATH, FINAL_OUTPUT_PATH)
    logging.info(f'Subtitles video created in {time() - start_time} seconds')
