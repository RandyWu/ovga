from app import app
from flask import Flask, session,render_template,request,redirect, url_for
from app.model.model import db,Event

@app.route('/editscores_landing', methods=['POST','GET'])
def editscores_landing():
    event_list = Event.query.all()

    if request.method == 'POST' and request.form["submit"]:
        session['edit_score_event'] = request.form.get("event_select")
        return redirect(url_for('editscore'))
        
    return render_template("editscores_landing.html", event_list=event_list)