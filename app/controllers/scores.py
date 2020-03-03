from app import app
from app.model.model import *
from flask import Flask, render_template

@app.route('/scores')
def scores():
    players = Player.query.all()
    users = User.query.all()
    return render_template("scores.html", player_name = players, users = users)