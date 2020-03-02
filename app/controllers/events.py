from app import app
from flask import Flask, render_template

@app.route('/events')
def events():
    return render_template("events.html")