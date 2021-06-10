from moviepy.editor import *
from moviepy.video.fx.resize import resize
import sounddevice as sd
import numpy as np
import display
import music
import queue
import threading
import time
import math
import sys

buffersize=30
blocksize=1024
q = queue.Queue(maxsize=buffersize)
event = threading.Event()

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


def playVideo(file="roll.mp4"):
    video = VideoFileClip(file)
    audio = video.audio
    video = resize(video, (20, 18))
    duration = video.duration  # == audio.duration, presented in seconds, float
    # note video.fps != audio.fps
    fps = audio.fps
    audio = audio.to_soundarray().astype('float32')
    step = (1/video.fps)
    audioblocks = []
    for t in range(int(duration * fps / blocksize)):
        audioblocks.append(audio[int(t*blocksize): int((t+1)*blocksize), :].flatten().tobytes())

    stream = sd.RawOutputStream(samplerate=fps, blocksize=blocksize, device=sd.default.device, channels=2,
                       dtype=np.float32, callback=callback, finished_callback=event.set)

    for x in range(buffersize):
        q.put_nowait(audioblocks[x])

    with stream:
        prev_frame = -1
        for t in range(buffersize, int(duration * fps / blocksize)):
            if t == len(audioblocks): break
            seconds = t*blocksize/fps
            frame = math.floor(seconds * video.fps)
            if frame > prev_frame:
                prev_frame = frame
                video_frame = video.get_frame(frame / video.fps)
                display.display(video_frame)
            q.put(audioblocks[t], timeout=0.1)
        event.wait()