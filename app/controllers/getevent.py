from app import app
from app.model.model import Event
from flask import Flask, render_template, request

@app.route('/get_events', methods=['POST', 'GET'])
def get_events():
    date_dict = {
        'Jan': '01',
        'Feb': '02',
        'Mar': '03',
        'Apr': '04',
        'May': '05',
        'Jun': '06',
        'Jul': '07',
        'Aug': '08',
        'Sep': '09',
        'Oct': '10',
        'Nov': '11',
        'Dev': '12'
    }

    unformated_date = request.form.get("date")
    trimmed_date = unformated_date.replace(',','').split(' ')
    trimmed_date[0] = date_dict[trimmed_date[0]]
    formated_date = trimmed_date[2] + '-' + trimmed_date[0] + '-' + trimmed_date[1]
    events = Event.query.filter_by(Date=formated_date).all()
    success = 'FALSE'

    if len(events) != 0:
        success = 'TRUE'
        
    return render_template("getevent.html", events=events, success=success)