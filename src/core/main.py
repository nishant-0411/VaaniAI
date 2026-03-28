import os
import signal
import sys

# Add the project root to sys.path so that 'src' can be imported correctly
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
from src.intelligence.memory import ConversationMemory
from src.intelligence.llm_client import LLMClient
from src.audio.input_audio import capture_audio_streaming
from src.audio.tts_engine import TTSEngine
from src.audio.stt_engine import STTEngine
from src.audio.audio_player import AudioPlayer
from src.utils.logger import get_logger

logger = get_logger(__name__)


class VoiceAssistant:
    def __init__(self):
        self.running = True
        self.state = "LISTENING"

        self.memory = ConversationMemory(max_messages=8)

        try:
            self.llm = LLMClient(self.memory)
        except TypeError:
            logger.warning("LLMClient doesn't accept memory, using default init")
            self.llm = LLMClient()

        self.tts = TTSEngine()
        self.stt = STTEngine()
        self.audio_player = AudioPlayer()
        self.audio_player.start()

    def handle_exit(self, signum, frame):
        logger.info("Shutting down gracefully...")
        self.running = False
        self.cleanup()
        sys.exit(0)

    def cleanup(self):
        logger.info("Cleaning up resources...")
        self.audio_player.shutdown()

    def run(self):
        print("=== Voice Assistant Started ===")
        print("Press Ctrl+C to exit\n")

        while self.running:
            try:
                self.state = "LISTENING"
                logger.info("STATE: LISTENING")

                try:
                    user_input = ""

                    for chunk in capture_audio_streaming():
                        print("chunk:", chunk)
                        if chunk:
                            transcribed_text = self.stt.transcribe(chunk)
                            if transcribed_text:
                                user_input += transcribed_text + " "
                        if len(user_input.strip()) > 0:
                            break
                except Exception as e:
                    logger.error(f"Audio capture failed: {e}")
                    user_input = input("You: ")

                if not user_input or not user_input.strip():
                    continue

                if self.state == "SPEAKING":
                    self.audio_player.stop()

                self.state = "THINKING"
                logger.info("STATE: THINKING")

                print("AI: ", end="", flush=True)

                full_response = ""

                for token in self.llm.get_response_stream(user_input):
                    print(token, end="", flush=True)
                    full_response += token

                print()

                self.state = "SPEAKING"
                logger.info("STATE: SPEAKING")

                try:
                    audio_bytes = self.tts.speak(full_response)
                    self.audio_player.add(audio_bytes)
                except Exception as e:
                    logger.error(f"TTS failed: {e}")

            except Exception as e:
                logger.error(f"Error in main loop: {e}")
                continue


if __name__ == "__main__":
    assistant = VoiceAssistant()

    signal.signal(signal.SIGINT, assistant.handle_exit)

    assistant.run()