import video
import music
import display
import numpy as np
import AudioUtils
import sys
import DJ

def main():
    music.folder = '/media/pi/F/music'
    DJ.loop('Elderbrook - Bird Song')

if __name__=="__main__":
    main()