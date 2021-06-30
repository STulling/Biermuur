import music
import numpy as np
import sys

def main():
    file = 'benee.wav'
    mPlayer = music.MusicPlayer(callback_function=None)
    mPlayer.playSound(file)

if __name__=="__main__":
    main()