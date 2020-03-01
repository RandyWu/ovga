from flask import Flask, render_template
app = Flask(__name__)


@app.route('/')
def hello():
    return "Hello World!"

@app.route('/scores')
def scores():
    return render_template("scores.html")

if __name__ == '__main__':
    app.run()
