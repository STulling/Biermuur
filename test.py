import video
import music
import display
import numpy as np
import AudioUtils
import sys
import DJ

def main():
    DJ.loop('lieblingsfach.wav', blocksize=int(sys.argv[1]))

if __name__=="__main__":
    main()