import os
from flask import Flask, request, jsonify
import yt_dlp
import whisper
import openai

# Set up the Flask application
app = Flask(__name__)

# Set your OpenAI API key
openai.api_key = api_key

# Function to download the audio of a YouTube video based on its video ID
def download(video_id: str) -> str:
    video_url = f'https://www.youtube.com/watch?v={video_id}'
    output_folder = 'audio'

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    ydl_opts = {
        'format': 'm4a/bestaudio/best',
        'outtmpl': os.path.join(output_folder, '%(id)s.%(ext)s'),
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

# Load the English transcription model
english_model = whisper.load_model("base.en")


# Function to transcribe the audio
def transcribe(file_path: str) -> str:
    transcription = english_model.transcribe(file_path, fp16=False)["text"]
    return transcription

# Function to generate a summary of the transcript using OpenAI's gpt-3.5-turbo model
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
    audio_path = download(video_id)
    transcript = transcribe(audio_path)
    summary = generate_summary(transcript)
    return jsonify({
        'transcription': transcript,
        'summary': summary
    })

@app.route('/api/video/<video_id>', methods=['GET'])
def get_video(video_id):
    # Logic to fetch and return video details based on the video_id
    # Replace with your own implementation
    video_details = {
        'video_id': video_id,
        'title': 'Sample Video',
        'duration': '10:30',
        'views': 100,
        # Add more details as per your requirements
    }
    return jsonify(video_details)

if __name__ == '__main__':
    app.run()