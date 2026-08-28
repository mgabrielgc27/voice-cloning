from pathlib import Path
from datetime import datetime
import threading
from audio.input import AudioInput
from audio.output import AudioOutput

CHANNELS = 1
SAMPLE_RATE = 44100
RAW_DATA_DIR = Path.cwd() / 'data/raw'

AudioInput = AudioInput(channels=CHANNELS, sample_rate=SAMPLE_RATE)
now = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
AudioOutput = AudioOutput(str(RAW_DATA_DIR / f'{now}.wav'), channels=CHANNELS, sample_rate=SAMPLE_RATE, sample_width=AudioInput.sample_width)

AudioInput.start_stream()

thread = threading.Thread(target=AudioInput.record)
thread.start()

while True:
    command = input('Enter "stop" to stop recording: ')
    print(f'Command received: {command}')
    if command.lower() == 'stop':
        print('Stopping recording...')
        AudioInput.recording = False
        break

thread.join()

AudioInput.stop_stream()
AudioInput.terminate()
AudioOutput.add_frames(AudioInput.frames)
AudioOutput.save_to_file()