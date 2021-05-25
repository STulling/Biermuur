from flask import Flask, render_template, request
from display import init, movingText, setStrip

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.form.get('clear'):
            print("Clearing")
            setStrip((0, 0, 0))
        elif request.form.get('show') and request.form.get('text'):
            print("showing: " + request.form.get('text'))
            movingText(request.form.get('text'), 0.04)
        else:
            return render_template("index.html")
    return render_template("index.html")


if __name__ == "__main__":
    init()
    app.run(debug=True)
