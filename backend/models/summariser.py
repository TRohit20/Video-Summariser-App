# Set your OpenAI API key
import openai

openai.api_key = "Use-your-own-API-Key"

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