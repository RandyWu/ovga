from app import app
from flask import Flask, render_template

@app.route('/delevent')
def delevent():
    return render_template("delevent.html")