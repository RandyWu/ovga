from app import app
from flask import Flask,session,render_template,request
from app.model.model import db,Event,Venue,Course

@app.route('/editevent_info', methods=['POST', 'GET'])
def editevent_info():
    if session['selected_event']:
        selected_event = int(session['selected_event'])

        event = Event.query.filter_by(EventId=selected_event).first()
        venue_list = Venue.query.all()
        event_course = event.CourseID
        event_venue = event.Venue_Id
        course_list = Course.query.filter_by(VenueID=event_venue).all()

        event_name = event.Name
        event_date = event.Date

        if request.method == 'POST' and request.form.get('submit') == 'submit':
            new_name = request.form.get("event_name")
            new_date = request.form.get("event_date")
            new_venue = int(request.form.get("venue_list"))
            new_course = int(request.form.get("course_list"))

            event.Name = new_name
            event.Date = new_date
            event.Venue_Id = new_venue
            event.CourseID = new_course
            db.session.commit()

            venue_list = Venue.query.all()
            course_list = Course.query.filter_by(VenueID=event_venue).all()

            return render_template(
                "editevent_info.html",
                event_name=new_name,
                event_date=new_date,
                event_venue=new_venue,
                event_course=new_course,
                venue_list=venue_list,
                course_list=course_list)
        
    return render_template(
        "editevent_info.html", 
        event_name=event_name, 
        event_date=event_date,
        event_venue=event_venue,
        event_course=event_course,
        venue_list=venue_list,
        course_list=course_list)