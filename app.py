from flask import Flask, render_template
<<<<<<< HEAD
=======
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)
>>>>>>> 46487d0d26c2d291822c9f76fbeed56e97e823b2

@app.route('/')
def hello():
    return "Hello World!"

@app.route('/scores')
def scores():
    return render_template("scores.html")

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
