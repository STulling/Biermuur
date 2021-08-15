import os
import random
import MusicPlayer

playlist_folder = os.path.join(os.environ["FLASK_MEDIA_DIR"], "playlists")


def load_playlist(name):
    with open(os.path.join(playlist_folder, name), 'r') as f:
        return [x.strip() for x in f.readlines()]


def shuffle_songs(song_list):
    MusicPlayer.playList(song_list)


def play(name):
    songs = load_playlist(name)
    shuffle_songs(songs)


def destroy(playlist_name):
    os.remove(os.path.join(playlist_folder, playlist_name))



def rename(playlist_name, new_name):
    songs = load_playlist(playlist_name)
    destroy(playlist_name)
    with open(os.path.join(playlist_folder, new_name), 'w') as f:
        f.writelines(songs)


def add_song(playlist_name, song_name):
    songs = load_playlist(playlist_name)
    print(songs)
    print(song_name)
    if song_name not in songs:
        with open(os.path.join(playlist_folder, playlist_name), 'a') as f:
            f.write(song_name + "\n")


def new(playlist_name):
    with open(os.path.join(playlist_folder, playlist_name), 'w') as f:
        f.close()


def remove_song(playlist_name, song_name):
    songs = load_playlist(playlist_name)
    songs.remove(song_name)
    with open(os.path.join(playlist_folder, playlist_name), 'w') as f:
        f.writelines(songs)


def list_playlists():
    return os.listdir(playlist_folder)
