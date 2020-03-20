from app import app
from flask import Flask, render_template

@app.route('/events_landing')
def events_landing():
    return render_template("events_landing.html")