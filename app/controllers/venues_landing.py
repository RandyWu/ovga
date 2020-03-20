from app import app
from flask import Flask, render_template

@app.route('/venues_landing')
def venues_landing():
    return render_template("venues_landing.html")