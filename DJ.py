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

def loop():
    keyboard.on_press(on_press)
    display.init()
    global mPlayer
    mPlayer = music.MusicPlayer()
    mPlayer.set_callback(AudioUtils.simple)
    mPlayer.playSound('lieblingsfach.wav')
