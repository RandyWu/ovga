from app import app
from flask import Flask, render_template

@app.route('/editscore')
def editscore():
    return render_template("editscore.html")