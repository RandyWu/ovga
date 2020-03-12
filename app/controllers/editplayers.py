from app import app
from flask import Flask, render_template

@app.route('/editplayers')
def editplayers():
    return render_template("editplayers.html")