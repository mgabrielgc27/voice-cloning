import wave
from .base import AudioOutput

class FileOutput(AudioOutput):
    def __init__(self, filename, channels=1, sample_width=2, sample_rate=44100):
        self.filename = filename
        self.channels = channels
        self.sample_width = sample_width
        self.sample_rate = sample_rate

        self.file = None

    def start(self) -> None:
        self.file = wave.open(self.filename, 'wb')
        self.file.setnchannels(self.channels)
        self.file.setsampwidth(self.sample_width)
        self.file.setframerate(self.sample_rate)

    def write(self, data: bytes) -> None:
        if self.file is None:
            raise RuntimeError("File is not opened.")
        self.file.writeframes(data)

    def stop(self) -> None:
        if self.file is not None:
            self.file.close()
            self.file = None

    def close(self) -> None:
        self.stop()