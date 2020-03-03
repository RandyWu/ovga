from app import app
from flask import Flask, render_template

@app.route('/')
@app.route('/login')
def login():
    return render_template("login.html")