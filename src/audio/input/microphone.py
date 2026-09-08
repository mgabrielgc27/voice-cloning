import pyaudio
from typing import Optional
from .base import AudioInput

class MicrophoneInput(AudioInput):
    def __init__(self, channels: int = 1, sample_rate: int = 48000, chunk_size: int = 1024, format: int = pyaudio.paInt16):
        self.channels = channels
        self.sample_rate = sample_rate
        self.chunk_size = chunk_size
        self.format = format
        self.audio_interface = pyaudio.PyAudio()
        self.sample_width = self.audio_interface.get_sample_size(self.format)
        self.stream: Optional[pyaudio.Stream] = None

    def start(self) -> None:
        if self.stream is not None:
            return # Stream is already running

        self.stream = self.audio_interface.open(
            format=self.format,
            channels=self.channels,
            rate=self.sample_rate,
            input=True,
            frames_per_buffer=self.chunk_size
        )

    def read(self) -> bytes:
        if self.stream is None:
            raise RuntimeError("Stream is not started.")

        #print(f"Read chunk number {len(self.frames)}: {len(data)} bytes.")
        return self.stream.read(self.chunk_size)

    def stop(self):
        if self.stream is None:
            return # Stream is not running

        self.stream.stop_stream()
        self.stream.close()
        self.stream = None

    def close(self):
        self.stop()
        self.audio_interface.terminate()