from src.audio.input_audio import list_microphones, capture_audio
from src.audio.stt_engine import STTEngine
from src.intelligence.llm_client import LLMClient

print("=== Available Microphones ===")
list_microphones()

MIC_INDEX = None

stt = STTEngine(use_whisper=False)
llm = LLMClient()

while True:
    print("\n=== Say something! ===")
    audio = capture_audio(mic_index=MIC_INDEX)

    if audio is None:
        print("No audio captured, check your microphone!")
        continue

    print("\n=== Transcribing... ===")
    text = stt.transcribe(audio)

    if not text:
        print("Could not understand, try speaking louder or clearer")
        continue

    print(f"\nYou said: {text}")
    print("\n=== Thinking... ===")
    response = llm.get_response(text)

    print(f"\nAI: {response}")