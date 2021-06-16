from flask import Flask, render_template, request, redirect, url_for
from flask_restful import Resource, Api
from flask_cors import CORS
from display import init, movingText, setStrip
from multiprocessing import Process
from datetime import datetime
import music
import video
import display
import sys
import os
import DJ

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
api = Api(app)
process = None
time = datetime.now()


def newProcess(prim, sec, curr_callback, action, args):
    init()
    display.primary = prim
    display.secondary = sec
    DJ.currentCallback = curr_callback
    if len(args) != 0:
        action(args[0])
    else:
        action()



def setAction(action, args):
    global process
    if process and process.is_alive():
        process.kill()
    process = Process(target=newProcess, args=(display.primary, display.secondary, DJ.currentCallback, action, args))
    process.start()


class Songs(Resource):
    def get(self):
        return music.listSongs()

class Play(Resource):
    def get(self, song_name):
        setAction(DJ.loop, (song_name, ))

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
}


class CommonControls(Resource):
    def get(self, action):
        if action in func_mappings:
            setAction(func_mappings[action], ())
        elif action == "update":
            update()


class DJControls(Resource):
    def get(self, action):
        if action in DJ.callbackNames:
            DJ.currentCallback.value = DJ.callbackNames.index(action)


api.add_resource(Songs, '/api/songs')
api.add_resource(Play, '/api/songs/play/<string:song_name>')
api.add_resource(SongAdder, '/api/songs/add/<string:song_name>')
api.add_resource(SongModifier, '/api/songs/<string:song_name>')
api.add_resource(CommonControls, '/api/common/<string:action>')
api.add_resource(Settings, '/api/settings/<string:setting>')
api.add_resource(DJControls, '/api/DJ/<string:action>')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.form.get('clear'):
            setAction(setStrip, (tuple([0, 0, 0]),))
        elif request.form.get('randomWoord'):
            setAction(display.randomwoord, ())
        elif request.form.get('regenboog'):
            setAction(display.rainbow, ())
        elif request.form.get('diamond_wipes'):
            setAction(display.diamond_wipes, ())
        elif request.form.get('random_pixel'):
            setAction(display.random_pixel, ())
        elif request.form.get('random_order_wipe'):
            setAction(display.random_order_wipe, ())
        elif request.form.get('show') and request.form.get('text'):
            print("showing: " + request.form.get('text'))
            setAction(movingText, (request.form.get('text'), 0.04, True))
        elif request.form.get('golf'):
            setAction(display.golf, ())
        elif request.form.get('lijnen'):
            setAction(display.lijnen, ())
        elif request.form.get('matrix'):
            setAction(display.matrix, ())
        elif request.form.get('set'):
            display.setTheme(request.form.get('primary'), request.form.get('secondary'))
        elif request.form.get('cirkels'):
            setAction(display.cirkels, ())
        elif request.form.get('histogram'):
            setAction(display.histogram, ())
        elif request.form.get('update'):
            update()
        elif request.form.get('spiraal'):
            setAction(display.spiraal, ())
        elif request.form.get('krat'):
            setAction(display.boxes, ())
        elif request.form.get('video'):
            setAction(video.playVideo, ())
        elif request.form.get('shuffle') and request.form.get('playlist'):
            setAction(music.shuffleplaylist, (request.form.get('playlist'),))
        elif request.form.get('download') and request.form.get('playlist') and request.form.get('song'):
            setAction(music.download, (request.form.get('song'),))
        return redirect(url_for('index'))
    return render_template("index.html", colors=display.getHTMLColors(), time=time.strftime("%d/%m/%Y %H:%M:%S"), playlists=music.listFolders())


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