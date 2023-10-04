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
    instructPrompt = """
                    Given below is the transcript of a video. Please provide a concise yet comprehensive summary that captures the main points, key discussions, and any notable insights or takeaways.

                    How to perform this task:
                    First, break the transcript into logical sections based on topic or theme. Then, generate a concise summary for each section. Finally, combine these section summaries into an overarching summary of the entire video. The combined summary is what you should return back to me.
                    Things to focus on and include in your final summary:
                    - Ensure to extract the key insights, theories, steps, revelations, opinions, etc discussed in the video. Ensure that the summary provides a clear roadmap for listeners who want to implement the advice or insights(if any) shared.
                    - Identify any controversial or heavily debated points in the video. Summarize the various perspectives presented, ensuring a balanced representation of the video or points in the video.
                    - Along with a content summary, describe the overall mood or tone of the video. Were there moments of tension, humor, or any other notable ambiance details?
  
                    Here is the video transcript:
                    """
    
    request = instructPrompt + transcript
    resp = openai.ChatCompletion.create(
        model="gpt-4-32k",
        messages=[
            {"role": "system", "content": "You are a helpful AI assistant that specialises in summarizing data."},
            {"role": "user", "content": request},
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


st.title('🔗 Summarize Video ')
 
with st.form(key='my_form'):
    video_source = st.selectbox('Select Video Source', ['YouTube', 'Vimeo'])
    video_id = st.text_input(label='Provide Video ID')
    submit_button = st.form_submit_button(label='Summarize')
 
if submit_button and video_id:
    st.write("Starting download process: ")
    
    if video_source == 'YouTube':
        audio_path = download_youtube(video_id)
    elif video_source == 'Vimeo':
        audio_path = download_vimeo(video_id)
    
    st.write("File downloaded to: ",audio_path)
    transcript = transcribe(audio_path)
    st.write("Original transcription: ",transcript)
    summary = generate_summary(transcript)
 
    st.write("summary: ")
    st.write(summary)
    print("Summary done")