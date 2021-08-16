import sys
import sounddevice as sd
import queue
import os
import numpy as np
from audio2numpy import open_audio
import display
import pickle
from wow_math import savgol_filter
import random
import threading
from Worker import Worker

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

class MusicPlayer():

    def __init__(self, callback_function=None, blocksize=1024):
        self.callback_function = callback_function
        self.blocksize = blocksize
        self.buffersize = 1000
        self.effectbuffer = queue.Queue(maxsize=self.buffersize)
        self.q = queue.Queue(maxsize=self.buffersize)
        self.volume = 1
        self.music_queue = []
        self.shuffle_choices = []
        self.workerqueue = queue.Queue(maxsize=3)
        self.worker = Worker(self.workerqueue)

    def set_callback(self, new_callback):
        self.callback_function = new_callback

    def process(self, data, highest_tone):
        self.callback_function(data, highest_tone)

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

    def load_song(self, file):
        print(f"Playing: {file}")
        song, samplerate = open_audio(file)
        print(samplerate)
        print(f"Read file")
        song = song.astype(np.float32)
        pklfile = os.path.join(folder, file + '.pkl')
        if os.path.exists(pklfile):
            with open(pklfile, 'rb') as f:
                rms_cache, color_cache = pickle.load(f)
        else:
            rms_cache = [np.sqrt(np.mean(song[i * self.blocksize:(i + 1) * self.blocksize, :] ** 2)) for i in
                              range(int(np.ceil(len(song) / self.blocksize)))]
            print(f"Loaded rms_cache")
            ffi_cache = [np.fft.fft(song[i * self.blocksize:(i + 1) * self.blocksize, 0])[
                              0:int(self.blocksize / 2)] / self.blocksize for i in
                              range(int(np.ceil(len(song) / self.blocksize)))]
            print(f"Loaded ffi_cache")
            ffi_cache = [np.abs(x)[11:61] for x in ffi_cache]
            highest_tones = savgol_filter([np.argmax(x) for x in ffi_cache], 21, 2)
            color_cache = [int(max(0, min(x * 10, 255)))/255 for x in highest_tones]
            print(f"Transformed ffi_cache")
            with open(pklfile, 'wb') as f:
                pickle.dump((rms_cache, color_cache), f)

        rms_max = max(rms_cache)
        song = (song / rms_max) * self.volume
        rms_cache = [x / rms_max for x in rms_cache]
        return song, rms_cache, color_cache

    def playPlaylist(self, songs):
        song_name = random.choice(songs)
        song, rms_cache, color_cache = self.load_song(song_name)
        i = 0
        for _ in range(self.buffersize):
            if (i+1)*self.blocksize > len(song):
                break
            data = song[i*self.blocksize:(i+1)*self.blocksize, :]
            i += 1
            self.q.put_nowait(data)  # Pre-fill queue
            self.effectbuffer.put_nowait((rms_cache[i], color_cache[i]))

        stream = sd.OutputStream(
            samplerate=44100, blocksize=self.blocksize,
            device=sd.default.device, channels=2, dtype='float32',
            callback=self.callback)
        stream.start()
        self.worker.start()
        print("00")

        while True:
            if i >= len(rms_cache):
                song_name = random.choice(songs)
                song, rms_cache, color_cache = self.load_song(song_name)
                i = 0
            data = song[i * self.blocksize:(i + 1) * self.blocksize, :]
            print("01")
            rms, color = self.effectbuffer.get()
            print("02")
            self.workerqueue.put((self.callback_function, rms, color))
            print("03")
            self.q.put(data, timeout=3)
            print("04")
            self.effectbuffer.put((rms_cache[i], color_cache[i]))
            print("05")
            i += 1

    def playSound(self, file):
        self.playPlaylist([file])
