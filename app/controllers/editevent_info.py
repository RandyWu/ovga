from app import app
from flask import Flask,session,render_template,request
from app.model.model import db,Event

@app.route('/editevent_info', methods=['POST', 'GET'])
def editevent_info():
    if session['selected_event']:
        selected_event = int(session['selected_event'])
        event = Event.query.filter_by(EventId=selected_event).first()

        event_name = event.Name
        event_date = event.Date

        if request.method == 'POST' and request.form.get('submit') == 'submit':
            new_name = request.form.get("event_name")
            new_date = request.form.get("event_date")

            event.Name = new_name
            event.Date = new_date
            db.session.commit()

            session['selected_event']= selected_event

            return render_template("editevent_info.html", event_name=new_name, event_date=new_date)
        
    return render_template("editevent_info.html", event_name=event_name, event_date=event_date)