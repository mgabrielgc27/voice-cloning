import wave
import numpy as np

class AudioOutput:
    def __init__(self, filename, channels=1, sample_width=2, sample_rate=44100):
        self.filename = filename
        self.channels = channels
        self.sample_width = sample_width
        self.sample_rate = sample_rate
        self.frames = []

    def add_frames(self, frames):
        self.frames.extend(frames)

    def save_to_file(self):
        with wave.open(self.filename, 'wb') as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.sample_width)
            wf.setframerate(self.sample_rate)
            wf.writeframes(b''.join(self.frames))