from pynput.keyboard import Key, Listener

import display
import music
import AudioUtils

mPlayer = None

def on_press(key):
    if key == Key.esc:
        mPlayer.set_callback(exit)
    if key.char == 'b':
        mPlayer.set_callback(AudioUtils.simple)
    if key.char == 's':
        mPlayer.set_callback(AudioUtils.sparkle)
    if key.char == 'r':
        mPlayer.set_callback(AudioUtils.ruit)

def loop():
    listener = Listener(on_press=on_press)
    listener.start()
    display.init()
    global mPlayer
    mPlayer = music.MusicPlayer()
    mPlayer.set_callback(AudioUtils.simple)
    mPlayer.playSound('lieblingsfach.wav')
