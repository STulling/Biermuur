import random

import sys
import sounddevice as sd
import queue
import threading
import os
import numpy as np
from audio2numpy import open_audio
import display
import pickle

folder = os.environ["FLASK_MEDIA_DIR"]


def download(name):
    command = f"youtube-dl -x -f bestaudio -x --audio-format mp3 -o \"{folder}/%(title)s.%(ext)s\" \"ytsearch1:{name}\""
    os.system(command)

def rename(old, new):
    os.rename(os.path.join(folder, old + '.mp3'), os.path.join(folder, new + '.mp3'))

def remove(file):
    os.remove(os.path.join(folder, file + '.mp3'))

def listFolders():
    return [x[0] for x in os.walk(folder)]

def listSongs():
    return [f[:-4] for f in os.listdir(folder) if f.endswith('.mp3')]

def shuffleplaylist(path):
    while True:
        song = random.choice([os.path.join(path, name) for path, subdirs, files in os.walk(path) for name in files])
        DJ.loop(song)


class MusicPlayer():

    def __init__(self, callback_function=None, blocksize=2048):
        self.callback_function = callback_function
        self.blocksize = blocksize
        self.buffersize = 500
        self.q = queue.Queue(maxsize=self.buffersize)
        self.empty_space = np.zeros((self.blocksize*self.buffersize, 2))
        self.rms_cache = []
        self.ffi_cache = []
        self.volume = 1

    def set_callback(self, new_callback):
        self.callback_function = new_callback

    def process(self, data):
        self.callback_function(data)

    def callback(self, outdata, frames, time, status):
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

    def playSound(self, file):
        print(f"Playing: {file}")
        song, samplerate = open_audio(file)
        print(f"Read file")
        song = np.append(song, self.empty_space, axis=0)
        channels = song.shape[1]
        song = song.astype(np.float32)
        pklfile = os.path.join(folder, file + '.pkl')
        if os.path.exists(pklfile):
            with open(pklfile, 'rb') as f:
                self.rms_cache, self.ffi_cache = pickle.load(f)
        else:
            self.rms_cache = [np.sqrt(np.mean(song[i*self.blocksize:(i+1)*self.blocksize, :]**2)) for i in range(int(np.ceil(len(song)/self.blocksize)))]
            print(f"Loaded rms_cache")
            self.ffi_cache = [np.fft.fft(song[i*self.blocksize:(i+1)*self.blocksize, 0])[0:int(self.blocksize/2)]/self.blocksize for i in
                              range(int(np.ceil(len(song) / self.blocksize)))]
            print(f"Loaded ffi_cache")
            self.ffi_cache = [np.abs(x)[11:] for x in self.ffi_cache]
            print(f"Transformed ffi_cache")
            with open(pklfile, 'wb') as f:
                pickle.dump((self.rms_cache, self.ffi_cache), f)

        rms_max = max(self.rms_cache)
        song = (song / max(self.rms_cache)) * self.volume
        self.rms_cache = [x / rms_max for x in self.rms_cache]
        i = 0
        x = 0
        for _ in range(self.buffersize):
            if (i+1)*self.blocksize > len(song):
                break
            data = song[i*self.blocksize:(i+1)*self.blocksize, :]
            i+=1
            self.q.put_nowait(data)  # Pre-fill queue

        stream = sd.OutputStream(
            samplerate=samplerate, blocksize=self.blocksize,
            device=sd.default.device, channels=channels, dtype='float32',
            callback=self.callback)
        stream.start()
        while (i+1)*self.blocksize < len(song):
            data = song[i * self.blocksize:(i + 1) * self.blocksize, :]
            i += 1
            if max(self.ffi_cache[x]) > 0.01:
                display.primary.value = display.wheel(min(np.argmax(self.ffi_cache[x]) * 3, 255))
            else:
                display.primary.value = display.wheel(0)
            if self.callback_function is not None:
                self.process(self.rms_cache[x])
            x += 1
            self.q.put(data, timeout=3)
        stream.stop()
        stream.close()
        self.q.queue.clear()
