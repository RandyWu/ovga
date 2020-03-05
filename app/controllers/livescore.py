from app import app
from app.model.model import *
from flask import Flask, render_template

@app.route('/livescore')
def livescore():
    return render_template("livescore.html")