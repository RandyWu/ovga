from app import app
from flask import Flask, render_template, redirect, flash, request, url_for
from app.controllers.forms import LoginForm
from app import login
from flask_login import current_user, login_user
from app.model.model import Admin, Player, load_user

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('You are already logged in.')
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(Email=form.email.data).first()
        player = Player.query.filter_by(Email=form.email.data).first()
        if (admin or player):
            #Login admin or player
            if((Admin.query.filter_by(Email=form.email.data, Password=form.password.data).first()) or (Player.query.filter_by(Email=form.email.data, Password=form.password.data).first())):
                flash('Successful Login')
                if admin:
                    login_user(admin)
                if player:
                    login_user(player)
                return redirect(url_for('index'))
            else:
                flash('Incorrect password')
                return redirect(url_for('login'))    
        else:
            flash('Invalid email')
            return redirect(url_for('login'))
    return render_template('login.html', title='Sign In', form=form)
from flask_login import logout_user, current_user

@app.route('/logout')
def logout():
    logout_user()
    return render_template('logout.html', title='Logout')
