import os
import random
import music
import MusicPlayer

playlist_folder = os.path.join(os.environ["FLASK_MEDIA_DIR"], "playlists")


def load_playlist(name):
    with open(os.path.join(playlist_folder, name), 'r') as f:
        return f.readlines()


def shuffle_songs(song_list):
    while True:
        try:
            song = random.choice(song_list)
            MusicPlayer.play(song)
        except:
            pass


def play_playlist(name):
    songs = load_playlist(name)
    shuffle_songs(songs)
