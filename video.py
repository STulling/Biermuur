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

buffersize=10
blocksize=1024
q = queue.Queue(maxsize=buffersize)
event = threading.Event()

def playVideo(file="roll.mp4"):
    video = VideoFileClip(file)
    audio = video.audio
    video = resize(video, (20, 18))
    duration = video.duration  # == audio.duration, presented in seconds, float
    # note video.fps != audio.fps
    stream = sd.RawOutputStream(samplerate=audio.fps, blocksize=audio.fps, device=sd.default.device, channels=2,
                       dtype=np.float32)
    fps = audio.fps
    audio = audio.to_soundarray().astype('float32')
    step = (1/video.fps)
    audioblocks = []
    videoblocks = []
    for t in range(int(duration / step)):
        audioblocks.append(audio[int(t*step*fps): int((t+1)*step*fps), :])
        
    with stream:
        prev_frame = -1
        for t in range(int(duration / step)):
            if t == len(audioblocks): break
            audio_frame = audioblocks[t]
            frame = math.floor(t * step * video.fps)
            if frame > prev_frame:
                prev_frame = frame
                video_frame = video.get_frame(frame / video.fps)
                display.display(video_frame)
            stream.write(audio_frame)