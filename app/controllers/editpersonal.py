from app import app
from flask import Flask, render_template

@app.route('/editpersonal')
def editpersonal():
    return render_template("editpersonal.html")