from app import app
from flask import Flask, render_template, redirect, flash, request, url_for
from flask_login import current_user
from app import login
from flask_login import current_user, login_user
from app.model.model import Admin, Player, User

@app.route('/admin')
def admin():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    user = User.query.filter_by(UserId=current_user.UserId).first()
    if user.Role != 'Admin':
        flash("Opps you don't have access to this page")
        return render_template("index.html")
    person = Player.query.filter_by(PlayerId=current_user.UserId).first()
    return render_template("admin.html", person=person)