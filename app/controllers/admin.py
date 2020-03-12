from app import app
from flask import Flask, render_template

@app.route('/admin')
def admin():
    return render_template("admin.html")