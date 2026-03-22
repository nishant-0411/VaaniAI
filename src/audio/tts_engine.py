import io
import requests
from gtts import gTTS
import os
from dotenv import load_dotenv

load_dotenv()

class TTSEngine:
    def __init__(self, mode = "gtts"):
        self.mode = mode
        self.api_key = os.getenv("ELEVENLABS_API_KEY")
        self.voice_id = os.getenv("ELEVENLABS_VOICE_ID")

    def speak(self, text:str):
        try:
            if self.mode == "elevenlabs" and self.api_key and self.voice_id:
                return self._elevenlabs_tts(text)
            else:
                return self._gtts_tts(text)

        except Exception as e:
            print("⚠️ TTS error, falling back to gTTS:", e)
            return self._gtts_tts(text)
    
    def _gtts_tts(self, text:str):
        tts = gTTS(text=text, lang="en") # Mp3 audio
        audio_buffer = io.BytesIO() # fake file (Memory Buffer)
        tts.write_to_fp(audio_buffer) # Writing Mp3 audio to that Memory Buffer
        return audio_buffer.getvalue()
    
    def _elevenlabs_tts(self, text:str):
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{self.voice_id}"
        response = requests.post(url, 
                    json={
                        "text": text
                    }, 
                    headers={
                        "xi-api-key": self.api_key,
                        "Content-Type": "application/json"
                    }
                )

        if response.status_code != 200:
            raise Exception(f"ElevenLabs error: {response.text}")

        return response.content
