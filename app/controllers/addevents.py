from app import app
from flask import Flask, render_template, request
from app.model.model import db,Venue,Event,Course

@app.route('/addevents/get_event', methods=['POST', 'GET'])
def get_events():
    date = request.form.get("date")
    events = Event.query.filter_by(Date=date).all()

    if len(events) != 0:
        success = 'TRUE'
    else:
        success = 'FALSE'
        
    return render_template("populate_list.html", events=events, success=success)

@app.route('/addevents/get_course', methods=['POST', 'GET'])
def get_course():
    venue_id = request.form.get("venue")
    course_list = Course.query.filter_by(VenueID=venue_id).all()

    if len(course_list) != 0:
        success = 'TRUE'
    else:
        success = 'FALSE'
        
    return render_template("get_courses.html", course_list=course_list, success=success)

@app.route('/addevents', methods=['POST', 'GET'])
def addevents():
    venue_list = Venue.query.all()

    if request.method == 'POST' and request.form["submit"]:

        selected_venue = int(request.form.get("venue_list"))
        selected_course = int(request.form.get("course_list"))
        venue_address = Venue.query.filter_by(VenueId=selected_venue).first().Address
        event_name = request.form.get("event_name")
        event_date = request.form.get("selected_date")

        new_event = Event(Venue_Id=selected_venue,Name=event_name,Address=venue_address,Date=event_date,CourseID=selected_course)
        db.session.add(new_event)
        db.session.commit()

    return render_template("addevents.html", venue_list = venue_list)