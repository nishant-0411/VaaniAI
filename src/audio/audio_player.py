import queue
import threading
import simpleaudio as sa
from pydub import AudioSegment
import io

class AudioPlayer:
    def __init__(self):
        self.audio_queue = queue.Queue()
        self.stop_flag = False
        self.running = True
        self.current_play = None
        self.thread = None

    def start(self):
        self.thread = threading.Thread(target=self._play_loop, daemon=True)
        self.thread.start()

    def add(self, audio_bytes):
        if audio_bytes:
            self.audio_queue.put(audio_bytes)

    def stop(self):
        print("Interrupt triggered")

        self.stop_flag = True

        while not self.audio_queue.empty():
            try:
                self.audio_queue.get_nowait()
            except queue.Empty:
                break

        if self.current_play:
            self.current_play.stop()

    def shutdown(self):
        """Graceful shutdown"""
        print("Shutting down AudioPlayer...")
        self.running = False

        self.audio_queue.put(None)

        if self.thread:
            self.thread.join()

    def _play_loop(self):
        while self.running:
            try:
                audio = self.audio_queue.get(timeout=1)

                if audio is None:
                    continue

                if self.stop_flag:
                    self.stop_flag = False
                    continue
                self._play(audio)

            except queue.Empty:
                continue
            except Exception as e:
                print("Playback loop error:", e)

    def _play(self, audio_bytes):
        try:
            audio = AudioSegment.from_file(io.BytesIO(audio_bytes), format="mp3")
            raw_data = audio.raw_data
            play_obj = sa.play_buffer(
                raw_data,
                num_channels=audio.channels,
                bytes_per_sample=audio.sample_width,
                sample_rate=audio.frame_rate
            )
            self.current_play = play_obj
            play_obj.wait_done()

        except Exception as e:
            print("Audio error:", e)