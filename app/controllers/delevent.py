from app import app
from flask import Flask,session,render_template,request
from app.model.model import db,Event,Player,PlayerDivision,Score

@app.route('/delevent', methods=['POST', 'GET'])
def delevent():
    if request.method == 'POST' and request.form["submit"]:
        event_id = request.form.get('event_select')

        removed_event = PlayerDivision.query.filter_by(Event_Id=removed_event).all()

    event_list = Event.query.all()
    return render_template("delevent.html", event_list=event_list)