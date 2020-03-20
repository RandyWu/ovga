from app import app
from flask import Flask, render_template

@app.route('/editevent_info')
def editevent_info():
    return render_template("editevent_info.html")