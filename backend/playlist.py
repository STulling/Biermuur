import os
import random
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


def play(name):
    songs = load_playlist(name)
    shuffle_songs(songs)


def add_song(playlist_name, song_name):
    with open(os.path.join(playlist_folder, playlist_name), 'a') as f:
        f.write(song_name + "\n")


def remove_song(playlist_name, song_name):
    songs = load_playlist(playlist_name)
    songs.remove(song_name)
    with open(os.path.join(playlist_folder, playlist_name), 'w') as f:
        f.writelines(songs)


def list_playlists():
    return os.listdir(playlist_folder)
