import os
import streamlit as st
import youtube_dl
import yt_dlp
import whisper
import openai
import ffmpeg
 
#set Azure openaI
openai.api_type = "azure"
openai.api_version = "2023-03-15-preview"
openai.api_type = "azure"
openai.api_base = ""
openai.api_key =""
os.environ["OPENAI_API_TYPE"] = "azure"
os.environ["OPENAI_API_KEY"] = ""
os.environ["OPENAI_API_BASE"] =openai.api_base
 
# Load the English transcription model
english_model = whisper.load_model("base.en")
 
# Function to transcribe the audio
def transcribe(file_path: str) -> str:
    transcription = english_model.transcribe(file_path, fp16=False)["text"]
    return transcription
 
# Function to generate a summary of the transcript using OpenAI's gpt-3.5-turbo model
def generate_summary(transcript: str) -> str:
    resp = openai.ChatCompletion.create(
        model="gpt-4-32k",
        messages=[
            {"role": "system", "content": "You are an AI assistant that helps in summarizing data."},
            {"role": "user", "content": f'Summarize this: {transcript}'},
        ]
    )
    return resp['choices'][0]['message']['content']
 

# Function to download the audio of a YouTube video based on its video ID
def download_youtube(video_id: str) -> str:
    video_url = f'https://www.youtube.com/watch?v={video_id}'
    output_folder = 'audio'

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    ydl_opts = {
        'format': 'm4a/bestaudio/best',
        'outtmpl': os.path.join(output_folder, f'{video_id}.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'm4a',
        }]
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        error_code = ydl.download([video_url])
        if error_code != 0:
            raise Exception('Failed to download video')

    return os.path.join(output_folder, f'{video_id}.m4a')

# Function to download the audio of a Vimeo video based on its video ID
def download_vimeo(video_id: str) -> str:
    video_url = f'https://vimeo.com/{video_id}'
    output_folder = 'audio'

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(output_folder, f'{video_id}.%(ext)s'),
        'postprocessors': [
            {
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'm4a',
            }
        ],
        'noplaylist': True,
        'nocheckcertificate': True,
        'ignoreerrors': True,
        'no_warnings': True,
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(video_url, download=False)
        audio_url = info_dict['formats'][0]['url']
        ydl.download([audio_url])

    return os.path.join(output_folder, f'{video_id}.m4a')
 
st.title('🔗 Summarize Youtube video ')
# st.write(ffmpeg.__file__)
#link = st.text_input('Provide youtube Video URL')
 
with st.form(key='my_form'):
    video_id = st.text_input(label='Provide youtube Video ID')
    submit_button = st.form_submit_button(label='Summarize')
 
if (len( video_id) > 0) :
    st.write("Starting download process: ")
    audio_path = download(video_id)
    st.write("File downloaded to: ",audio_path)
    transcript = transcribe(audio_path)
    st.write("Original transcription: ",transcript)
    summary = generate_summary(transcript)
 
    # filters out all the files with "mp4" extension
    #mp4files = video.filter('mp4')
    #d_video = video.get(mp4files[-1].extension,mp4files[-1].resolution)  
    st.write("summary: ")
    st.write(summary)
    #st.write("file path",d_video)
    print("Download done")
   