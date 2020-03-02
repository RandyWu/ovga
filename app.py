from flask import Flask, render_template, url_for, request, redirect
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html');

@app.route('/events')
def events():
    return render_template('events.html');