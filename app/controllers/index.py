from app import app
from flask import Flask, render_template

@app.route('/')
def hello():
    return render_template("index.html")