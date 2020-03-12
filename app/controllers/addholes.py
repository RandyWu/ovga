from app import app
from flask import Flask, render_template

@app.route('/addholes')
def addholes():
    return render_template("addholes.html")