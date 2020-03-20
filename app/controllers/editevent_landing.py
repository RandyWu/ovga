from app import app
from flask import Flask, render_template

@app.route('/editevent_landing')
def editevent_landing():
    return render_template("editevent_landing.html")