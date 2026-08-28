import pyaudio

class AudioInput:
    def __init__(self, channels=1, sample_rate=44100, chunk_size=1024, format=pyaudio.paInt16):
        self.channels = channels
        self.sample_rate = sample_rate
        self.chunk_size = chunk_size
        self.format = format
        self.audio_interface = pyaudio.PyAudio()
        self.sample_width = self.audio_interface.get_sample_size(self.format)
        self.stream = None
        self.frames = []
        self.recording = True

    def start_stream(self):
        if self.stream is not None:
            return # Stream is already running

        self.stream = self.audio_interface.open(
            format=self.format,
            channels=self.channels,
            rate=self.sample_rate,
            input=True,
            frames_per_buffer=self.chunk_size
        )

    def read_chunk(self):
        if self.stream is None:
            raise RuntimeError("Stream is not started.")

        data = self.stream.read(self.chunk_size)
        self.frames.append(data)
        #print(f"Read chunk number {len(self.frames)}: {len(data)} bytes.")

    def record(self):
        print("Recording started.")
        self.recording = True

        while self.recording:
            self.read_chunk()

        print("Recording stopped.")

    def stop_stream(self):
        if self.stream is None:
            return # Stream is not running

        self.stream.stop_stream()
        self.stream.close()

    def terminate(self):
        self.audio_interface.terminate()