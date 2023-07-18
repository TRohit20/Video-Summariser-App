from flask import Blueprint, request, jsonify
from audio.downloader import download_youtube, download_vimeo
from backend.audio.downloader import download_brightcove
from models.transcription import transcribe
from models.summariser import generate_summary

transcribe_route = Blueprint('transcribe_route', __name__)

@transcribe_route.route('/api/transcribe', methods=['POST'])
def transcribe_handler():
    try:
        video_id = request.form['videoId']
        video_source = request.form['videoSource']

        if video_source == 'youtube':
            audio_path = download_youtube(video_id)
        elif video_source == 'vimeo':
            audio_path = download_vimeo(video_id)
        elif video_source == 'brightcove':
            audio_path = download_brightcove(video_id)
        else:
            return jsonify({'error': 'Invalid video source'}), 400

        transcript = transcribe(audio_path)
        summary = generate_summary(transcript)

        return jsonify({
            'transcription': transcript,
            'summary': summary
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
