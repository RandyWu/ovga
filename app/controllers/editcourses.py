from app import app
from flask import Flask, render_template

@app.route('/editcourses')
def editcourses():
    return render_template("editcourses.html")