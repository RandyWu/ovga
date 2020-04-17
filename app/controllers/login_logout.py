from app import app
from flask import Flask, render_template, redirect, flash, request, url_for
from app.controllers.forms import LoginForm
from app import login
from flask_login import current_user, login_user, logout_user
from app.model.model import Admin, Player, User

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method != 'POST':
        return render_template('login.html', title='Sign In', form=form)
    if current_user.is_authenticated:
        flash('You are already logged in.')
        return redirect(url_for('index'))
        
    form = LoginForm(request.form)

    if form.validate_on_submit():
        # do player query then get user info
        user = User.query\
            .join(Player, Player.PlayerId==User.UserId)\
            .filter_by(Email=form.email.data).first()
        if (user != None):
            #Login admin or player
            flash('Successful Login')
            if user.Role == 'Admin':
                login_user(user)
                return redirect(url_for('admin'))
            elif user.Role == 'Player':
                login_user(user)
                return redirect(url_for('players')) 
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return render_template('logout.html', title='Logout')
