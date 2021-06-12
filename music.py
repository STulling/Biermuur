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
import audioop
from pydub import AudioSegment, effects

simulated = False

try:
    import pygame
    simulated = True
except Exception:
    pass

folder = "/media/pi/F/music"


def download(folder, name):
    command = f"youtube-dl -x -f bestaudio -x --audio-format wav -o \"{folder}/%(title)s.%(ext)s\" \"ytsearch1:{name}\""
    os.system(command)


def listFolders():
    return [x[0] for x in os.walk(folder)]


def shuffleplaylist(path):
    while True:
        song = random.choice([os.path.join(path, name) for path, subdirs, files in os.walk(path) for name in files])
        DJ.loop(song)


class MusicPlayer():

    buffersize = 200
    blocksize = 1024
    q = queue.Queue(maxsize=buffersize)
    event = threading.Event()

    def __init__(self, callback_function=None):
        self.callback_function = callback_function

    def set_callback(self, new_callback):
        self.callback_function = new_callback

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
        data = np.frombuffer(data, np.float32)[::2]
        if self.callback_function is not None:
            x = threading.Thread(self.callback_function, (np.sqrt(np.mean(data**2))))
            x.start()

    def playSound(self, file):
        print(f"Playing: {file}")
        self.event.clear()
        song, samplerate = sf.read(file)
        channels = song.shape[1]
        song = song.astype(np.float32)
        song = song / np.max(np.abs(song))
        i = 0
        for _ in range(self.buffersize):
            if (i+1)*self.blocksize > len(song):
                break
            data = song[i*self.blocksize:(i+1)*self.blocksize, :].flatten().tobytes()
            i+=1
            self.q.put_nowait(data)  # Pre-fill queue

        stream = sd.RawOutputStream(
            samplerate=samplerate, blocksize=self.blocksize,
            device=sd.default.device, channels=channels, dtype='float32',
            callback=self.callback, finished_callback=self.event.set)
        with stream:
            timeout = self.blocksize * self.buffersize / samplerate
            while (i+1)*self.blocksize < len(song):
                data = song[i * self.blocksize:(i + 1) * self.blocksize, :].flatten().tobytes()
                i += 1
                self.q.put(data, timeout=timeout)
                if simulated:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            exit()
            self.event.wait()  # Wait until playback is finished
        self.q.queue.clear()
