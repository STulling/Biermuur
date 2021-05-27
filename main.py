from flask import Flask, render_template, request, redirect, url_for
from display import init, movingText, setStrip
from multiprocessing import Process
import display
import sys
import os

app = Flask(__name__)
process = None

def setAction(action, args):
    global process
    if process and process.is_alive():
        process.kill()
    process = Process(target=action, args=args)
    process.start()


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
        return redirect(url_for('index'))
    return render_template("index.html", colors=display.getHTMLColors())


def update():
    os.system("git pull")


if __name__ == "__main__":
    try:
        init()
    except NameError:
        print("No display hooked up, ignoring...")
    try:
        app.run(host="0.0.0.0", debug=True)
    except KeyboardInterrupt:
        if process and process.is_alive():
            process.kill()
        sys.exit(0)