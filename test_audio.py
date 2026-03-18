from src.audio.input_audio import list_microphones, capture_audio
from src.audio.stt_engine import STTEngine

print("=== Available Microphones ===")
list_microphones()

MIC_INDEX = None 

print("\n=== Say something! ===")
audio = capture_audio(mic_index=MIC_INDEX)

if audio is None:
    print("No audio captured, check your microphone!")
else:
    print("\n=== Transcribing... ===")
    stt = STTEngine(use_whisper=False)  
    text = stt.transcribe(audio)

    if text:
        print(f"\nYou said: {text}")
    else:
        print("Could not understand, try speaking louder or clearer")