import keyboard

import display
import music
import AudioUtils
import os

mPlayer = None

def on_press(key):
    if key.name == 'esc':
        mPlayer.set_callback(exit)
    if key.name == 'b':
        mPlayer.set_callback(AudioUtils.simple)
    if key.name == 's':
        mPlayer.set_callback(AudioUtils.sparkle)
    if key.name == 'r':
        mPlayer.set_callback(AudioUtils.ruit)
    if key.name == 'c':
        mPlayer.set_callback(AudioUtils.cirkel)
    if key.name == 'w':
        mPlayer.set_callback(AudioUtils.wave)


def loop(file):
    file = os.path.join(music.folder, file + '.wav')
    keyboard.on_press(on_press)
    display.init()
    global mPlayer
    mPlayer = music.MusicPlayer(callback_function=AudioUtils.simple)
    mPlayer.playSound(file)
