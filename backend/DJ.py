import keyboard

import display
import music
import AudioUtils

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


def loop(file):
    keyboard.on_press(on_press)
    display.init()
    global mPlayer
    mPlayer = music.MusicPlayer(callback_function=AudioUtils.simple)
    mPlayer.playSound(file)
