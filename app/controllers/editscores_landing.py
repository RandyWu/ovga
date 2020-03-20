from app import app
from flask import Flask, render_template

@app.route('/editscores_landing')
def editscores_landing():
    return render_template("editscores_landing.html")