import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    LLM_MODEL = os.getenv("LLM_MODEL", "phi3")
    OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")

    STT_MODEL = os.getenv("STT_MODEL", "base")
    TTS_ENGINE = os.getenv("TTS_ENGINE", "pyttsx3")

    SAMPLE_RATE = int(os.getenv("SAMPLE_RATE", 16000))
    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 1024))

    MAX_HISTORY = int(os.getenv("MAX_HISTORY", 10))
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

config = Config()