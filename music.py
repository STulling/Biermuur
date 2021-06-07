import random

import display
import sys
import sounddevice as sd
import soundfile as sf
import queue
import threading
import os
import numpy as np

buffersize=10
blocksize=1024
q = queue.Queue(maxsize=buffersize)
event = threading.Event()

folder = "/media/pi/F/music"


def download(folder, name):
    command = f"youtube-dl -x -f bestaudio -x --audio-format wav -o \"{folder}/%(title)s.%(ext)s\" \"ytsearch1:{name}\""
    os.system(command)


def listFolders():
    return [x[0] for x in os.walk(folder)]


def callback(outdata, frames, time, status):
    assert frames == blocksize
    if status.output_underflow:
        print('Output underflow: increase blocksize?', file=sys.stderr)
        raise sd.CallbackAbort
    assert not status
    try:
        data = q.get_nowait()
    except queue.Empty:
        print('Buffer is empty: increase buffersize?', file=sys.stderr)
        raise sd.CallbackAbort
    if len(data) < len(outdata):
        outdata[:len(data)] = data
        outdata[len(data):] = b'\x00' * (len(outdata) - len(data))
        raise sd.CallbackStop
    else:
        outdata[:] = data


def playSound(file):
    print(f"Playing: {file}")
    with sf.SoundFile(file) as f:
        for _ in range(buffersize):
            data = f.buffer_read(blocksize, dtype='float32')
            if not data:
                break
            q.put_nowait(data)  # Pre-fill queue

        stream = sd.RawOutputStream(
            samplerate=f.samplerate, blocksize=blocksize,
            device=sd.default.device, channels=f.channels, dtype='float32',
            callback=callback, finished_callback=event.set)
        with stream:
            timeout = blocksize * buffersize / f.samplerate
            while data:
                data = f.buffer_read(blocksize, dtype='float32')
                q.put(data, timeout=timeout)
                display.setStrip(display.secondary, False)
                display.setAmountColor(int(np.max(np.frombuffer(data)) * 200000), display.getIfromRGB(display.primary))
            event.wait()  # Wait until playback is finished
    q.queue.clear()


def shuffleplaylist(path):
    while True:
        song = random.choice([os.path.join(path, name) for path, subdirs, files in os.walk(path) for name in files])
        playSound(song)