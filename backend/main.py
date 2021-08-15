from flask import Flask, render_template, request, redirect, url_for, make_response, Response
from flask_restful import Resource, Api
from flask_cors import CORS
from display import init, movingText, setStrip
from multiprocessing import Process
import music
import display
import sys
import os
import MusicPlayer
import json
import playlist

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
api = Api(app)
process = None

func_mappings = {
    'clear': display.clear,
    'random_word': display.randomwoord,
    'rainbow': display.rainbow,
    'diamond_wipes': display.diamond_wipes,
    'random_pixel_wipe': display.random_pixel,
    'random_order_wipe': display.random_order_wipe,
    'golf': display.golf,
    'lijnen': display.lijnen,
    'matrix': display.matrix,
    'cirkels': display.cirkels,
    'histogram': display.histogram,
    'spiraal': display.spiraal,
    'krat': display.boxes,
    'dobbelsteen': display.dobbelsteen,
}


def newProcess(prim, sec, curr_callback, action, args):
    init()
    display.primary = prim
    display.secondary = sec
    MusicPlayer.currentCallback = curr_callback
    if len(args) != 0:
        action(args[0])
    else:
        action()


def setAction(action, args):
    global process
    if process and process.is_alive():
        process.kill()
    process = Process(target=newProcess,
                      args=(display.primary, display.secondary, MusicPlayer.currentCallback, action, args))
    process.start()


class Play(Resource):
    def get(self, song_name):
        setAction(MusicPlayer.play, (song_name,))


class SongAdder(Resource):
    def get(self, song_name):
        music.download(song_name)


class SongModifier(Resource):
    def put(self, song_name):
        newName = request.form['data']
        music.rename(song_name, newName)

    def delete(self, song_name):
        music.remove(song_name)


class Settings(Resource):
    def put(self, setting):
        newVal = request.form['data']
        if setting == 'primary':
            display.primary.value = display.getIfromRGB(display.HTMLColorToRGB(newVal))
        if setting == 'secondary':
            display.secondary.value = display.getIfromRGB(display.HTMLColorToRGB(newVal))


class CommonControls(Resource):
    def get(self, action):
        if action in func_mappings:
            setAction(func_mappings[action], ())
        elif action == "update":
            update()


class DJControls(Resource):
    def get(self, action):
        if action in MusicPlayer.callbackNames:
            MusicPlayer.currentCallback.value = MusicPlayer.callbackNames.index(action)


class PlaylistControls(Resource):
    def get(self, action, playlist_name):
        if action == "play":
            setAction(playlist.play, (playlist_name,))
        elif action == "list":
            return playlist.list_playlists()

    def put(self, action, playlist_name):
        song_name = request.form['data']
        if action == "add":
            playlist.add_song(playlist_name, song_name)
        else:
            pass

    def delete(self, action, playlist_name):
        song_name = request.form['data']
        if action == "remove":
            playlist.remove_song(playlist_name, song_name)
        else:
            pass


api.add_resource(Play, '/api/songs/play/<string:song_name>')
api.add_resource(SongAdder, '/api/songs/add/<string:song_name>')
api.add_resource(SongModifier, '/api/songs/<string:song_name>')
api.add_resource(CommonControls, '/api/common/<string:action>')
api.add_resource(Settings, '/api/settings/<string:setting>')
api.add_resource(DJControls, '/api/DJ/<string:action>')
api.add_resource(PlaylistControls, '/api/playlists/<string:action>/<string:playlist_name>')


@app.route('/')
def index():
    return "use port 3000"

# extreem cringe
@app.route('/api/songs')
def songs():
    return music.listSongs()

def update():
    if process and process.is_alive():
        process.kill()
    os.system("git -C .. pull")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        music.folder = sys.argv[1]
    try:
        app.run(host="0.0.0.0", debug=True)
    except KeyboardInterrupt:
        if process and process.is_alive():
            process.kill()
        sys.exit(0)
