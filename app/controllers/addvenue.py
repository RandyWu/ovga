from app import app
from flask import Flask, render_template, redirect, flash, request, url_for
from flask_login import current_user
from app import login
from flask_login import current_user, login_user
from app.model.model import Admin, Player, User, db, Venue

@app.route('/addvenue', methods=['POST','GET'])
def addvenue():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    user = User.query.filter_by(UserId=current_user.UserId).first()
    if user.Role != 'Admin':
        flash("Opps you don't have access to this page")
        return render_template("index.html")
    if request.method == 'POST':
        venue_name = request.form.get("venue_name")
        venue_address = request.form.get("venue_address")

        new_venue = Venue(Name=venue_name,Address=venue_address)
        db.session.add(new_venue)
        db.session.commit()
    
    return render_template("addvenue.html")