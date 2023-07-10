import os
from flask import Flask, request, jsonify
import whisper
import openai
import yt_dlp
import youtube_dl

# Set up the Flask application
app = Flask(__name__)

# Set your OpenAI API key
openai.api_key = "Use-your-own-API-Key"

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

# Load the English transcription model
english_model = whisper.load_model("base.en")

# Function to transcribe the audio
def transcribe(file_path: str) -> str:
    transcription = english_model.transcribe(file_path, fp16=False)["text"]
    return transcription

# Function to generate a summary of the transcript
def generate_summary(transcript: str) -> str:
    resp = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f'Summarize this: {transcript}'},
        ]
    )
    return resp['choices'][0]['message']['content']

# API route to handle transcription and summarization
@app.route('/api/transcribe', methods=['POST'])
def transcribe_route():
    video_id = request.form['videoId']
    video_source = request.form['videoSource']

    if video_source == 'youtube':
        audio_path = download_youtube(video_id)
    elif video_source == 'vimeo':
        audio_path = download_vimeo(video_id)
    else:
        return jsonify({'error': 'Invalid video source'})

    transcript = transcribe(audio_path)
    summary = generate_summary(transcript)

    return jsonify({
        'transcription': transcript,
        'summary': summary
    })

if __name__ == '__main__':
    app.run()