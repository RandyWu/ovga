from app import app
from flask import Flask, render_template

@app.route('/editplayerpersonal')
def editplayerpersonal():
    return render_template("editplayerpersonal.html")