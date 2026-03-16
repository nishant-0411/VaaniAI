from utils.logger import get_logger
import speech_recognition as sr

logger = get_logger(__name__)
recogniser = sr.Recognizer()

def list_microphones():
    logger.info("Listing available microphones")
    mics = sr.Microphone.list_microphone_names()
    for index, name in enumerate(mics):
        logger.info(f"Mic {index}: {name}")
        print(f"{index}: {name}")
    return mics

def get_microphone(mic_index=None):
    try:
        if mic_index is None:
            logger.info("Using default microphone")
            return sr.Microphone()
        
        logger.info(f"Using microphone index {mic_index}")
        return sr.Microphone(device_index=mic_index)
    except Exception as e:
        logger.error(f"Microphone error: {e}")
        raise

def capture_audio(mic_index=None):
    try:
        with get_microphone(mic_index) as source:
            logger.info("Adjusting for ambient noise")
            recogniser.adjust_for_ambient_noise(source)
            logger.info("Listening for speech...")
            audio = recogniser.listen(source)
        logger.info("Audio captured successfully")
        return audio
    except Exception as e:
        logger.error(f"Audio capture failed: {e}")
        raise
