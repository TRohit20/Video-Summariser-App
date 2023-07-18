import os

import requests
import youtube_dl
import yt_dlp

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

# Function to download the audio of a Brightcove video based on its video ID
def download_brightcove(video_id: str) -> str:
    output_folder = 'audio'

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Make a request to Brightcove API to get the video metadata
    url = f'https://api.brightcove.com/services/library'
    params = {
        'command': 'find_video_by_reference_id',
        'reference_id': video_id,
        'video_fields': 'renditions'
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise Exception('Failed to fetch Brightcove video metadata')
    
    video_data = response.json()

    # Find the highest-quality audio rendition
    audio_url = None
    max_bitrate = 0
    for rendition in video_data.get('renditions', []):
        if 'audio' in rendition.get('type', '').lower() and rendition.get('encoding_rate', 0) > max_bitrate:
            audio_url = rendition.get('url')
            max_bitrate = rendition.get('encoding_rate', 0)

    if not audio_url:
        raise Exception('Failed to find audio rendition in Brightcove video')

    # Download the audio using the found URL
    response = requests.get(audio_url)
    if response.status_code != 200:
        raise Exception('Failed to download Brightcove video audio')

    audio_path = os.path.join(output_folder, f'{video_id}.m4a')
    with open(audio_path, 'wb') as file:
        file.write(response.content)

    return audio_path