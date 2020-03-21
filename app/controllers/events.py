from app import app
from app.model.model import Event
from flask import Flask, render_template, jsonify, request

@app.route('/events')
def events():
    upcoming_events = Event.query.order_by(Event.Date.desc()).limit(10).all()
    return render_template("events.html", upcoming_events = upcoming_events)