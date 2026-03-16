import speech_recognition as sr
from utils.logger import get_logger

logger = get_logger(__name__)
recogniser = sr.Recognizer()

class STTEngine:
    def __init__(self):
        logger.info("STT Engine initialized")
    
    def transcribe(self, audio):
        try:
            logger.info("Starting transcription")
            text = recogniser.recognize_google(audio)
            if not text.strip():
                logger.warning("Empty transcription received")
                return None

            logger.info(f"Transcription result: {text}")
            return text
        
        except sr.UnknownValueError:
            logger.warning("Speech not understood")
            return None
        
        except sr.RequestError as e:
            logger.error(f"STT API request failed: {e}")
            return None
        
        except Exception as e:
            logger.error(f"Unexpected STT error: {e}")
            return None