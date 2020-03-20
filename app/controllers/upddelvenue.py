from app import app
from flask import Flask, render_template

@app.route('/upddelvenue')
def upddelvenue():
    return render_template("upddelvenue.html")