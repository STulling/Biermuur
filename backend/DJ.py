import music
import AudioUtils
import os
import multiprocessing

callbacks = {
    "sparkle": AudioUtils.sparkle,
    "bars": AudioUtils.simple,
    "circle": AudioUtils.cirkel,
    "diamond": AudioUtils.ruit,
    "wave": AudioUtils.wave,
    "lightning": AudioUtils.bliksem,
    "quit": exit,
}
callbackNames = list(callbacks.keys())
callbackFunctions = list(callbacks.values())

mPlayer = None
currentCallback = multiprocessing.Value('i', 0)


def callback(rms):
    callbackFunctions[currentCallback.value](rms)


def loop(file):
    file = os.path.join(music.folder, file + '.mp3')
    global mPlayer
    mPlayer = music.MusicPlayer(callback_function=callback)
    mPlayer.playSound(file)
