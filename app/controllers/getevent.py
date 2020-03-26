# from app import app
# from app.model.model import Event
# from flask import Flask, render_template, request

# @app.route('/get_events', methods=['POST', 'GET'])
# def get_events():
#     date = request.form.get("date")
#     events = Event.query.filter_by(Date=date).all()

#     if len(events) != 0:
#         success = 'TRUE'
#     else:
#         success = 'FALSE'
        
#     return render_template("getevent.html", events=events, success=success)