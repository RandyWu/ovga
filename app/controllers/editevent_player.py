from app import app
from flask import Flask, render_template

@app.route('/editevent_player')
def editevent_player():
    return render_template("editevent_player.html")