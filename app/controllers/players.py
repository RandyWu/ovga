from app import app
from flask import Flask, render_template

@app.route('/players')
def players():
    return render_template("players.html")