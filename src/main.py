import threading
from pathlib import Path
from datetime import datetime
from audio.input import MicrophoneInput
from audio.output import FileOutput

CHANNELS = 1
SAMPLE_RATE = 44100
RAW_DATA_DIR = Path.cwd() / 'data/raw'

audio_input = MicrophoneInput(channels=CHANNELS, sample_rate=SAMPLE_RATE)
audio_input.start()

frame_buffer = []

recording = True
def record_audio():
    global recording
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

now = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
filename = str(RAW_DATA_DIR / f'{now}.wav')
audio_output = FileOutput(filename, channels=CHANNELS, sample_rate=SAMPLE_RATE, sample_width=audio_input.sample_width)
audio_output.start()
audio_output.write(b''.join(frame_buffer))
audio_output.close()