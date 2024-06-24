import whisper
from moviepy.editor import *
from deep_translator import GoogleTranslator
import logging
from time import time
from dotenv import dotenv_values

# load the environment variables
config = dotenv_values('.env')
VIDEOS_PATH = config['VIDEOS_PATH']
OUTPUT_PATH = config['OUTPUT_PATH']
TRANSLATE = config['TRANSLATE'] == 'True'
LANGUAGE_CODES = config['LANGUAGE_CODES'].split(",")
ORIGINAL_SUBTITLES = config['ORIGINAL_SUBTITLES'] == 'True'
WHISPER_MODEL_SIZE = config['WHISPER_MODEL_SIZE']

# load the whisper model
MODEL = whisper.load_model(name=WHISPER_MODEL_SIZE, download_root='whisper_models').to('cuda')

RTL_LANGUAGES = ['ar', 'iw']

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
def save_as_srt(segments, file_path, rtl=False):
    # check if a file exists with the same name as the file_name and delete it if it does
    if os.path.exists(file_path):
        os.remove(file_path)

    with open(file_path, "w") as file:
        for i, segment in enumerate(segments):
            start_time = format_srt_time(segment['start'])
            end_time = format_srt_time(segment['end'])
            text = segment['text']
            file.write(f'{i + 1}\n')
            file.write(f'{start_time} --> {end_time}\n')
            if rtl:
                text = text.strip()
                file.write(f'\u202b{text}\u202c\n\n')
            else:
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

def transcribe(audio_path):
    result = MODEL.transcribe(audio_path, fp16=False)
    return result['segments']

def translate(segments, target_language):
    translated_segments = []
    for segment in segments:
        translated_text = GoogleTranslator(source='auto', target=target_language).translate(segment['text'])
        translated_segment = {
            'start': segment['start'],
            'end': segment['end'],
            'text': translated_text
        }
        translated_segments.append(translated_segment)
    return translated_segments


def process_video(video_path):
    # get video name
    video_file_name = video_path.split('/')[-1]
    video_name = video_file_name.split('.')[0]
    video_output_directory = os.path.join(OUTPUT_PATH, video_name)
    if not os.path.exists(video_output_directory):
        os.makedirs(video_output_directory)
        
    video_path = os.path.join(VIDEOS_PATH, video_file_name)
    audio_path = os.path.join(video_output_directory, f'{video_name}.wav')
    # iw is Hebrew
    iw_srt_path = os.path.join(video_output_directory, f'iw_{video_name}.srt')

    start_time = time()
    logging.info('Extracting audio from video...')
    extract_audio_from_video(video_path, audio_path)
    logging.info(f'Audio extracted in {time() - start_time} seconds')

    start_time = time()
    logging.info('Transcribing audio...')
    segments = transcribe(audio_path)
    logging.info(f'Audio transcribed in {time() - start_time} seconds')
    logging.info(f'Saving iw segments as SRT...')
    save_as_srt(segments, iw_srt_path, rtl=True)

    srt_files_paths = {}
    
    if TRANSLATE:
        for language_code in LANGUAGE_CODES:
            language_srt_path = os.path.join(video_output_directory, f'{language_code}_{video_name}.srt')
            start_time = time()
            logging.info(f'Translating segments to {language_code}...')
            translated_segments = translate(segments, language_code)
            logging.info(f'Segments transtaled to {language_code} in {time() - start_time} seconds')
            
            start_time = time()
            logging.info(f'Saving {language_code} segments as SRT...')
            save_as_srt(translated_segments, language_srt_path, rtl=language_code in RTL_LANGUAGES)

            srt_files_paths[language_code] = language_srt_path

    # apply subtitles to video
    for language_code, srt_path in srt_files_paths.items():
        final_output_path = os.path.join(video_output_directory, f'{language_code}_{video_name}.mp4')
        start_time = time()
        logging.info(f'Creating subtitles video for {language_code}...')
        create_subtitles_video(video_path, audio_path, srt_path, final_output_path)
        logging.info(f'Subtitles video created for {language_code} in {time() - start_time} seconds')

    # create subtitles video for iw
    if ORIGINAL_SUBTITLES:
        final_output_path = os.path.join(video_output_directory, f'iw_{video_name}.mp4')
        start_time = time()
        logging.info(f'Creating subtitles video for iw...')
        create_subtitles_video(video_path, audio_path, iw_srt_path, final_output_path)
        logging.info(f'Subtitles video created for iw in {time() - start_time} seconds')


def main():
    logging.basicConfig(level=logging.INFO)

    # list all videos in the videos directory
    videos_files_paths = os.listdir(VIDEOS_PATH)

    for video_path in videos_files_paths:
        process_video(video_path)

if __name__ == '__main__':
    main()