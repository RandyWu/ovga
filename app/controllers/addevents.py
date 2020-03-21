from app import app
from flask import Flask, render_template, request
from app.model.model import db,Venue,Event

@app.route('/addevents', methods=['POST', 'GET'])
def addevents():
    venue_list = Venue.query.all()
    
    # if request.method == 'POST' and request.form["submit"]:

    #     selected_venue = int(request.form.get("selectedVenue"))
    #     venue_address = Venue.query.filter_by(VenueId=selected_venue).first().Address
    #     event_name = request.form.get("event_name")
    #     event_date = request.form.get("selected_date")

    #     new_event = Event(Venue_Id=selected_venue,Name=event_name,Address=venue_address,Date=event_date)
    #     db.session.add(new_event)
    #     db.session.commit()

    return render_template("addevents.html", venue_list = venue_list)