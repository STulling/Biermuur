from flask import Flask, render_template, request
from display import init, movingText, setStrip
from multiprocessing import Process
import display

app = Flask(__name__)
process = None


def setAction(action, args):
    global process
    if process:
        if process.is_alive():
            process.terminate()
    process = Process(target=action, args=args)
    process.start()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.form.get('clear'):
            print("Clearing")
            setAction(setStrip, (0, 0, 0))
        elif request.form.get('regenboog'):
            setAction(display.rainbow, ())
        elif request.form.get('show') and request.form.get('text'):
            print("showing: " + request.form.get('text'))
            setAction(movingText, (request.form.get('text'), 0.04))
        else:
            return render_template("index.html")
    return render_template("index.html")


if __name__ == "__main__":
    init()
    app.run(host="0.0.0.0", debug=True)
