from app import app
from flask import Flask, render_template, redirect, flash, request, url_for
from app.controllers.forms import LoginForm
from app import login
from flask_login import current_user, login_user
from app.model.model import Admin, Player

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(Email=form.email.data).first()
        player = Player.query.filter_by(Email=form.email.data).first()
        if (admin or player):
            return "hi"
        else:
            flash('Invalid username or password')
            return redirect(url_for('login'))
        # if user is None or not user.check_password(form.password.data):
        #     flash('Invalid username or password')
        #     
        # return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)