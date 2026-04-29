import os

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("ELEVEN_API_KEY")


def generate_voice(text, voice_id, filename):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

    headers = {"xi-api-key": API_KEY, "Content-Type": "application/json"}

    data = {"text": text, "voice_settings": {"stability": 0.3, "similarity_boost": 0.9}}

    response = requests.post(url, json=data, headers=headers)

    with open(filename, "wb") as f:
        f.write(response.content)

    return filename
