import wave
from typing import Optional
from .base import AudioInput

class FileInput(AudioInput):
    def __init__(self, filename: str, chunk_size: int = 1024):
        self.filename = filename
        self.chunk_size = chunk_size
        self.file: Optional[wave.Wave_read] = None
        self.sample_width: Optional[int] = None
        self.channels: Optional[int] = None
        self.sample_rate: Optional[int] = None

    def start(self) -> None:
        self.file = wave.open(self.filename, 'rb')
        self.channels = self.file.getnchannels()
        self.sample_width = self.file.getsampwidth()
        self.sample_rate = self.file.getframerate()

    def read(self) -> bytes:
        if self.file is None:
            raise RuntimeError("File is not opened.")
        return self.file.readframes(self.chunk_size)

    def stop(self) -> None:
        if self.file is None:
            return  # File is not opened

        self.file.close()
        self.file = None

    def close(self) -> None:
        self.stop()