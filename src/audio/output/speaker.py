import pyaudio
from .base import AudioOutput

class SpeakerOutput(AudioOutput):
    def __init__(self, channels=1, sample_rate=44100, sample_width=2, chunk_size=1024):
        self.channels = channels
        self.sample_rate = sample_rate
        self.chunk_size = chunk_size
        self.sample_width = sample_width
        self.audio_interface = pyaudio.PyAudio()
        self.format = self.audio_interface.get_format_from_width(self.sample_width)
        self.stream = None

    def start(self) -> None:
        if self.stream is not None:
            return  # Stream is already running

        self.stream = self.audio_interface.open(
            format=self.format,
            channels=self.channels,
            rate=self.sample_rate,
            output=True
        )

    def write(self, data: bytes) -> None:
        if self.stream is None:
            raise RuntimeError("Stream is not started.")

        self.stream.write(data)

    def stop(self) -> None:
        if self.stream is None:
            return  # Stream is not running

        self.stream.stop_stream()
        self.stream.close()
        self.stream = None

    def close(self) -> None:
        self.audio_interface.terminate()