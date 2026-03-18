import os
import tempfile
import speech_recognition as sr
from src.utils.logger import get_logger

logger = get_logger(__name__)
recogniser = sr.Recognizer()

try:
    import whisper
    WHISPER_AVAILABLE = True
    logger.info("Whisper is available")
except ImportError:
    WHISPER_AVAILABLE = False
    logger.warning("Whisper not installed, will use Google STT")


class STTEngine:
    def __init__(self, use_whisper=False, whisper_model="base"):
        self.use_whisper = use_whisper and WHISPER_AVAILABLE

        if self.use_whisper:
            logger.info(f"Loading Whisper '{whisper_model}' model...")
            self.model = whisper.load_model(whisper_model)
            logger.info("Whisper model ready!")
        else:
            self.model = None
            logger.info("Using Google STT")

    
    def transcribe(self, audio):
        if self.use_whisper:
            return self._whisper_transcribe(audio)
        else:
            return self._google_transcribe(audio)
        
    def _google_transcribe(self, audio):
        try:
            logger.info("Transcribing with Google...")
            text = recogniser.recognize_google(audio)

            if not text.strip():
                logger.warning("Empty result from Google STT")
                return None
            
            logger.info(f"Result: {text}")
            return text

        except sr.UnknownValueError:
            logger.warning("Google STT couldn't understand the audio")
            return None

        except sr.RequestError as e:
            logger.error(f"Google STT request failed (no internet?): {e}")
            return None
        
    def _whisper_transcribe(self, audio):
        try:
            logger.info("Transcribing with Whisper...")

            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
                tmp.write(audio.get_wav_data())
                tmp_path = tmp.name
            
            result = self.model.transcribe(tmp_path)
            os.remove(tmp_path)

            text = result["text"].strip()

            if not text:
                logger.warning("Empty result from Whisper")
                return None
            
            logger.info(f"Result: {text}")
            return text

        except Exception as e:
            logger.error(f"Whisper failed: {e}")
            return None