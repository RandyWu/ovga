from app import app
from flask import Flask,session,render_template,request
from app.model.model import db,Event,Player,PlayerDivision,Score

@app.route('/delevent', methods=['POST', 'GET'])
def delevent():
    if request.method == 'POST' and request.form["submit"]:
        event_id = int(request.form.get('event_select'))

        removed_event = Event.query.filter_by(EventId=event_id).first()
        removed_divisions = PlayerDivision.query.filter_by(Event_Id=event_id).all()
        removed_scores = Score.query.filter_by(EventID=event_id).all()

        if removed_event:
            db.session.delete(removed_event)
        if removed_divisions:
            db.session.delete(removed_scores)
        if removed_scores:
            for score in removed_scores:
                db.session.delete(score)

        rawr = request.form
        db.session.commit()

    event_list = Event.query.all()
    return render_template("delevent.html", event_list=event_list)