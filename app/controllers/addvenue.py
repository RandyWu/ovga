from app import app
from flask import Flask, render_template

@app.route('/addvenue')
def addvenue():
    return render_template("addvenue.html")