import queue
import threading
import simpleaudio as sa
from pydub import AudioSegment
import io

class AudioPlayer:
    def __init__(self):
        self.audio_queue = queue.Queue()
        self.stop_flag = False
        self.current_play = None

    def start(self):
        threading.Thread(target=self._play_loop, daemon=True).start()

    def add(self, audio_bytes):
        self.audio_queue.put(audio_bytes)

    def stop(self):
        print("🛑 Interrupt triggered")
        self.stop_flag = True

        while not self.audio_queue.empty():
            self.audio_queue.get()

        if self.current_play:
            self.current_play.stop()

    def _play_loop(self):
        while True:
            audio = self.audio_queue.get()

            if self.stop_flag:
                self.stop_flag = False
                continue

            if audio:
                self._play(audio)

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