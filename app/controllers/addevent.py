from app import app
from flask import Flask, render_template

@app.route('/addevent')
def addevent():
    return render_template("addevent.html")