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
    "mond": AudioUtils.mond,
    "fill": AudioUtils.fill,
    "quit": exit,
}
callbackNames = list(callbacks.keys())
callbackFunctions = list(callbacks.values())

mPlayer = None
currentCallback = multiprocessing.Value('i', 1)


def callback(rms, pitch):
    callbackFunctions[currentCallback.value](rms, pitch)


def loop(file):
    file = os.path.join(music.folder, file + '.mp3')
    global mPlayer
    mPlayer = music.MusicPlayer(callback_function=callback)
    mPlayer.playSound(file)
