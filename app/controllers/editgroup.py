from app import app
from flask import Flask, render_template

@app.route('/editgroup')
def editgroup():
    return render_template("editgroup.html")