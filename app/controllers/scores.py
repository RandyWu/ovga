from app import app
from flask import Flask, render_template

@app.route('/scores')
def scores():
    return render_template("scores.html")