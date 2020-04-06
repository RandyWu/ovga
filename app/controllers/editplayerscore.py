from app import app
from flask import Flask, render_template

@app.route('/editplayerscore')
def editplayerscore():
    return render_template("editplayerscore.html")