import os

from dotenv import load_dotenv

import openai
from pathlib import Path 
load_dotenv()


class VoiceOver:
    def __init__(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")
    def create_voiceover(self,text):
       response = openai.audio.speech.create(
           model="tts-1",
           voice="nova",
           input=text
       )
       Path("output.mp3").write_bytes(response.content)
       
v =VoiceOver()
v.create_voiceover("Hello guys how are tou")