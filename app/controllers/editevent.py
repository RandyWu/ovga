from app import app
from flask import Flask, render_template

@app.route('/editevent')
def editevent():
    return render_template("editevent.html")