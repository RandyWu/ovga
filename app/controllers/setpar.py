from app import app
from flask import Flask, render_template

@app.route('/setpar')
def setpar():
    return render_template("setpar.html")