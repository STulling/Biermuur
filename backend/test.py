import video
import music
import display
import numpy as np
import AudioUtils
import sys
import DJ

def main():
    file = 'benee.wav'
    mPlayer = music.MusicPlayer(callback_function=None)
    mPlayer.playSound(file)

if __name__=="__main__":
    main()