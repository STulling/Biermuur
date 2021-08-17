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
import concurrent.futures

folder = os.environ["FLASK_MEDIA_DIR"]


def load_song(file, blocksize, volume):
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
        rms_cache = [np.sqrt(np.mean(song[i * blocksize:(i + 1) * blocksize, :] ** 2)) for i in
                     range(int(np.ceil(len(song) / blocksize)))]
        print(f"Loaded rms_cache")
        ffi_cache = [np.fft.fft(song[i * blocksize:(i + 1) * blocksize, 0])[
                     0:int(blocksize / 2)] / blocksize for i in
                     range(int(np.ceil(len(song) / blocksize)))]
        print(f"Loaded ffi_cache")
        ffi_cache = [np.abs(x)[11:61] for x in ffi_cache]
        highest_tones = savgol_filter([np.argmax(x) for x in ffi_cache], 21, 2)
        color_cache = [int(max(0, min(x * 10, 255))) / 255 for x in highest_tones]
        print(f"Transformed ffi_cache")
        with open(pklfile, 'wb') as f:
            pickle.dump((rms_cache, color_cache), f)

    rms_max = max(rms_cache)
    song = (song / rms_max) * volume
    rms_cache = [x / rms_max for x in rms_cache]
    return song, rms_cache, color_cache

def download(name):
    command = f"youtube-dl -x -f bestaudio -x --audio-format mp3 --postprocessor-args \"-ar 44100 -ac 2\" -o \"{folder}/%(title)s.%(ext)s\" \"ytsearch1:{name}\""
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

    def playPlaylist(self, song_names):
        with concurrent.futures.ProcessPoolExecutor() as executor:
            song, rms_cache, color_cache = load_song(random.choice(song_names), self.blocksize, self.volume)
            future = executor.submit(load_song, random.choice(song_names), self.blocksize, self.volume)
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

            # load 1 song
            # load second song in background
            # use second song then load third song
            # etc.

            while True:
                if i >= len(rms_cache) - 1:
                    song, rms_cache, color_cache = future.result()
                    future = executor.submit(load_song, random.choice(song_names), self.blocksize, self.volume)
                    i = 0
                data = song[i * self.blocksize:(i + 1) * self.blocksize, :]
                rms, color = self.effectbuffer.get()
                display.primary.value = display.wheel(int(color * 255))
                self.process(rms, color)
                self.q.put(data, timeout=3)
                self.effectbuffer.put((rms_cache[i], color_cache[i]))
                i += 1

    def playSound(self, file):
        self.playPlaylist([file])
