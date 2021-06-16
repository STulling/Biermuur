import keyboard

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


def on_press(key):
    if key.name == 'esc':
        currentCallback.value = callbackNames.index('quit')
    if key.name == 'b':
        currentCallback.value = callbackNames.index('bars')
    if key.name == 's':
        currentCallback.value = callbackNames.index('sparkle')
    if key.name == 'r':
        currentCallback.value = callbackNames.index('diamond')
    if key.name == 'c':
        currentCallback.value = callbackNames.index('circle')
    if key.name == 'w':
        currentCallback.value = callbackNames.index('wave')
    if key.name == 'l':
        currentCallback.value = callbackNames.index('lightning')


def callback(rms):
    callbackFunctions[currentCallback.value](rms)


def loop(file):
    file = os.path.join(music.folder, file + '.wav')
    keyboard.on_press(on_press)
    global mPlayer
    mPlayer = music.MusicPlayer(callback_function=callback)
    mPlayer.playSound(file)
