from app import app
from flask import Flask, session,render_template,request,redirect, url_for
from app.model.model import db,Event


@app.route('/editevent_landing', methods=['POST', 'GET'])
def editevent_landing():
    events_list = Event.query.all()

    if request.method == 'POST':
        session['selected_event'] = int(request.form.get('event_select'))

        if request.form.get('submit') == 'event':
            return redirect(url_for('editevent_info'))
        
        if request.form.get('submit') == 'player':
            return redirect(url_for('editevent_player'))

    return render_template('editevent_landing.html', events_list=events_list)