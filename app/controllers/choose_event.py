from app import app
from flask import Flask, render_template

@app.route('/choose_event')
def choose_event():
    return render_template("choose_event.html")