from flask import Flask, render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)

@app.route('/')
def hello():
    return "Hello World!"

@app.route('/scores')
def scores():
    return render_template("scores.html")

if __name__ == '__main__':
    app.run()
