from app import app
from flask import Flask, render_template

@app.route('/editplayerinfo')
def editplayerinfo():
    return render_template("editplayerinfo.html")