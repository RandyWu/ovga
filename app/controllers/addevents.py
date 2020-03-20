from app import app
from flask import Flask, render_template

@app.route('/addevents')
def addevents():
    return render_template("addevents.html")