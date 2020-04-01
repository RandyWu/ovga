from app import app
from flask import Flask, render_template

@app.route('/courses_landing')
def courses_landing():
    return render_template("courses_landing.html")