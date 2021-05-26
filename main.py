from flask import Flask, render_template, request
from display import init, movingText, setStrip
from multiprocessing import Process
import display
import sys

app = Flask(__name__)
process = None

def setAction(action, args):
    global process
    if process and process.is_alive():
        process.terminate()
    process = Process(target=action, args=args)
    process.start()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.form.get('clear'):
            setAction(setStrip, (tuple([0, 0, 0]),))
        elif request.form.get('randomWoord'):
            setAction(display.randomwoord(), ((),))
        elif request.form.get('regenboog'):
            setAction(display.rainbow, ())
        elif request.form.get('diamond_wipes'):
            setAction(display.diamond_wipes, ())
        elif request.form.get('show') and request.form.get('text'):
            print("showing: " + request.form.get('text'))
            setAction(movingText, (request.form.get('text'), 0.04, True))
        elif request.form.get('golf'):
            setAction(display.golf(), ((),))
        else:
            return render_template("index.html")
    return render_template("index.html")


if __name__ == "__main__":
    try:
        init()
    except NameError:
        print("No display hooked up, ignoring...")
    try:
        app.run(host="0.0.0.0", debug=True)
    except KeyboardInterrupt:
        if process and process.is_alive():
            process.terminate()
        sys.exit(0)
