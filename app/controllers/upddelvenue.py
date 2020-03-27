from app import app
from flask import Flask,session,render_template,request
from app.model.model import db,Venue

@app.route('/upddelvenue', methods=['POST', 'GET'])
def upddelvenue():
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
            
            venue_list = Venue.query.all()
            return render_template("upddelvenue.html", venue_list=venue_list)

        if action == 'remove':
            db.session.delete(venue)
            db.session.commit()

            venue_list = Venue.query.all()
            return render_template("upddelvenue.html", venue_list=venue_list)

    venue_list = Venue.query.all()
    return render_template("upddelvenue.html", venue_list=venue_list)