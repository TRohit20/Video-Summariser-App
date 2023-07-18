import os
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