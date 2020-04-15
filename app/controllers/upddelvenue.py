from app import app
from flask import Flask, render_template, redirect, flash, request, url_for, jsonify
from flask_login import current_user
from app import login
from flask_login import current_user, login_user
from app.model.model import Admin, Player, User, db,Venue

@app.route('/upddelvenue', methods=['POST', 'GET'])
def upddelvenue():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    user = User.query.filter_by(UserId=current_user.UserId).first()
    if user.Role != 'Admin':
        flash("Opps you don't have access to this page")
        return render_template("index.html")

    if request.method == 'POST':
        action = request.form.get('submit')
        selected_venue = int(request.form.get('select_venue'))
        venue = Venue.query.filter_by(VenueId=selected_venue).first()

        if action == 'update':
            venue_name = request.form.get('venue_name')
            venue_address = request.form.get('venue_address')

            venue.Name = venue_name
            venue.Address = venue_address
            db.session.commit()

        if action == 'remove':
            db.session.delete(venue)
            db.session.commit()

    venue_list = Venue.query.all()
    if len(venue_list) != 0:
        success = 'TRUE'
    else:
        success = 'FALSE'
    return render_template("upddelvenue.html", venue_list=venue_list, success=success)

@app.route('/getvenueinfo', methods=['POST', 'GET'])  
def getvenueinfo():
    venue_id = request.form['select_venue']
    venue = Venue.query.filter_by(VenueId=venue_id).first()
    venue_name = venue.Name
    venue_address = venue.Address
    
    return jsonify({'venue_name':venue_name, 'venue_address':venue_address})