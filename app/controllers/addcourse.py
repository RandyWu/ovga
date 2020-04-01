from app import app
from flask import Flask, render_template

@app.route('/addcourse')
def addcourse():
    return render_template("addcourse.html")