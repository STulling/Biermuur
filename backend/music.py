import random

import DJ
import display
import sys
import sounddevice as sd
import soundfile as sf
import queue
import threading
import os
import numpy as np

folder = os.environ["FLASK_MEDIA_DIR"]


def download(name):
    command = f"youtube-dl -x -f bestaudio -x --audio-format wav -o \"{folder}/%(title)s.%(ext)s\" \"ytsearch1:{name}\""
    os.system(command)

def rename(old, new):
    os.rename(os.path.join(folder, old + '.wav'), os.path.join(folder, new + '.wav'))

def remove(file):
    os.remove(os.path.join(folder, file + '.wav'))

def listFolders():
    return [x[0] for x in os.walk(folder)]

def listSongs():
    return [f[:-4] for f in os.listdir(folder) if f.endswith('.wav')]

def shuffleplaylist(path):
    while True:
        song = random.choice([os.path.join(path, name) for path, subdirs, files in os.walk(path) for name in files])
        DJ.loop(song)


class MusicPlayer():

    def __init__(self, callback_function=None, blocksize=2048):
        self.callback_function = callback_function
        self.blocksize = blocksize
        self.buffersize = 200
        self.q = queue.Queue(maxsize=self.buffersize)
        self.event = threading.Event()

    def set_callback(self, new_callback):
        self.callback_function = new_callback

    def process(self, data):
        self.callback_function(np.sqrt(np.mean(data**2)))

    def callback(self, outdata, frames, time, status):
        print(status)
        assert frames == self.blocksize
        if status.output_underflow:
            print('Output underflow: increase blocksize?', file=sys.stderr)
            raise sd.CallbackAbort
        assert not status
        try:
            data = self.q.get_nowait()
        except queue.Empty:
            print('Buffer is empty: increase buffersize?', file=sys.stderr)
            raise sd.CallbackAbort
        if len(data) < len(outdata):
            outdata[:len(data)] = data
            outdata[len(data):] = b'\x00' * (len(outdata) - len(data))
            raise sd.CallbackStop
        else:
            outdata[:] = data
        if self.callback_function is not None:
            self.process(data)

    def playSound(self, file):
        print(f"Playing: {file}")
        self.event.clear()
        print('lets goo -3')
        song, samplerate = sf.read(file)
        channels = song.shape[1]
        print('lets goo -2')
        song = song.astype(np.float32)
        song = song / np.max(np.abs(song))
        print('lets goo -1')
        i = 0
        for _ in range(self.buffersize):
            if (i+1)*self.blocksize > len(song):
                break
            data = song[i*self.blocksize:(i+1)*self.blocksize, :]
            i+=1
            self.q.put_nowait(data)  # Pre-fill queue
        print('lets goo 0')

        stream = sd.OutputStream(
            samplerate=samplerate, blocksize=self.blocksize,
            device=sd.default.device, channels=channels, dtype='float32',
            callback=self.callback, finished_callback=self.event.set)
        print('lets goo')
        with stream:
            print('lets goo 2')
            timeout = 1
            while (i+1)*self.blocksize < len(song):
                print('lets goo 3')
                data = song[i * self.blocksize:(i + 1) * self.blocksize, :]
                i += 1
                self.q.put(data, timeout=timeout)
            print('what u doing here?')
            self.event.wait()
        self.q.queue.clear()
