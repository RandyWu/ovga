from app import app
from flask import Flask,session,render_template,request,redirect,url_for
from app.model.model import db,Event,PlayerDivision
from flask_login import current_user, login_user

@app.route('/choose_event', methods = ['POST','GET'])
def choose_event():
    user = current_user.UserId

    if request.method == 'POST' and request.form['submit']:
        selected_event = int(request.form.get('event_select'))
        return redirect(url_for('scores'))

    registered_events = PlayerDivision.query.filter_by(Player_Id=user).all()
    registered_players = PlayerDivision.query.filter_by(Player_Id=user).distinct().all()

    events = []
    for event in registered_events:
        e = Event.query.filter_by(EventId=event.Event_Id).first()
        event_id = e.EventId
        event_info = e.Name + " - " + e.Address 
        events.append((event_id,event_info))

    return render_template("choose_event.html", events=events)