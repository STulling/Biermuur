import music
import AudioUtils
import os
import multiprocessing

currentCallback = multiprocessing.Value('i', 1)

callbacks = {
    "sparkle": AudioUtils.sparkle,
    "bars": AudioUtils.simple,
    "circle": AudioUtils.cirkel,
    "diamond": AudioUtils.ruit,
    "wave": AudioUtils.wave,
    "slow wave": AudioUtils.slow_wave,
    "mond": AudioUtils.mond,
    "fill": AudioUtils.fill,
    "snake": AudioUtils.snake,
    "quit": exit,
}
callbackNames = list(callbacks.keys())
callbackFunctions = list(callbacks.values())

mPlayer = music.MusicPlayer(callback_function=
                            lambda rms, pitch: callbackFunctions[currentCallback.value](rms, pitch))


def play(file):
    file = os.path.join(music.folder, file + '.mp3')
    mPlayer.playSound(file)
