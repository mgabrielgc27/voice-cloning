import sys
from pathlib import Path
from datetime import datetime
from audio.output import SpeakerOutput

RAW_DATA_DIR = Path.cwd() / 'data/raw'
CHUNK_SIZE = 1024

channels = 1
sample_rate = 44100
sample_width = 2
frame_buffer = []

if(len(sys.argv) > 1):
    from audio.input import FileInput

    filename = sys.argv[1]
    print(f'Reading wave file: ${filename}')

    audio_input = FileInput(filename, chunk_size=CHUNK_SIZE)
    audio_input.start()

    channels = audio_input.channels
    sample_rate = audio_input.sample_rate
    sample_width = audio_input.sample_width

    while len(data := audio_input.read()):
        frame_buffer.append(data)

    print('Complete')

else:
    import threading
    from audio.input import MicrophoneInput
    from audio.output import FileOutput

    audio_input = MicrophoneInput(channels=channels, sample_rate=sample_rate, chunk_size=CHUNK_SIZE)
    audio_input.start()

    def record_audio():
        global recording
        recording = True
        print("Recording started.")
        while recording:
            frame_buffer.append(audio_input.read())

    thread = threading.Thread(target=record_audio)
    thread.start()

    while True:
        command = input('Enter "stop" to stop recording: ')
        print(f'Command received: {command}')
        if command.lower() == 'stop':
            print('Stopping recording...')
            recording = False
            break

    thread.join()

    def save_audio(frame_buffer):
        now = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        filename = str(RAW_DATA_DIR / f'{now}.wav')
        audio_output = FileOutput(filename, channels=channels, sample_width=audio_input.sample_width, sample_rate=sample_rate)
        audio_output.start()
        audio_output.write(b''.join(frame_buffer))
        audio_output.close()

    save_audio(frame_buffer)

def play_audio(frame_buffer: list):
    audio_output = SpeakerOutput(channels=channels, sample_rate=sample_rate, sample_width=sample_width, chunk_size=CHUNK_SIZE)
    audio_output.start()

    print('Playing audio...')
    while len(frame_buffer):
        audio_output.write(frame_buffer.pop(0))

    print('Stopped.')
    audio_output.stop()
    audio_output.close()

play_audio(frame_buffer)