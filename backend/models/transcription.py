import whisper

# Load the English transcription model
english_model = whisper.load_model("base.en")

# Function to transcribe the audio
def transcribe(file_path: str) -> str:
    transcription = english_model.transcribe(file_path, fp16=False)["text"]
    return transcription