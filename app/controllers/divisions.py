from app import app, login
from datetime import date
from flask_login import current_user, login_user
from flask import Flask, session, render_template, jsonify, request, redirect, flash, url_for
from app.model.model import *

@app.route('/divisions/home', methods=['POST','GET'])
def divisions():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    user = User.query.filter_by(UserId=current_user.UserId).first()
    if user.Role != 'Admin':
        flash("Opps you don't have access to this page")
        return render_template("index.html")

    event_list = Event.query.all()

    if request.method == 'POST':
        session['selected_event'] = int(request.form.get('event_select'))

        if request.form.get('submit') == 'info':
            return redirect(url_for('edit_divisions'))
        
        if request.form.get('submit') == 'addrem':
            return redirect(url_for('add_divisions'))

    return render_template("/divisions/divisions_home.html", event_list=event_list)

@app.route('/divisions/edit')
def edit_divisions():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    user = User.query.filter_by(UserId=current_user.UserId).first()
    if user.Role != 'Admin':
        flash("Opps you don't have access to this page")
        return render_template("index.html")

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
                "/divisions/edit_divisions.html",
                event_name=new_name,
                event_date=new_date,
                event_venue=new_venue,
                event_course=new_course,
                venue_list=venue_list,
                course_list=course_list)
        
    return render_template(
        "/divisions/edit_divisions.html", 
        event_name=event_name, 
        event_date=event_date,
        event_venue=event_venue,
        event_course=event_course,
        venue_list=venue_list,
        course_list=course_list)

    return render_template("/divisions/edit_divisions.html")


@app.route('/divisions/add', methods=['POST', 'GET'])
def add_divisions():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    user = User.query.filter_by(UserId=current_user.UserId).first()
    if user.Role != 'Admin':
        flash("Opps you don't have access to this page")
        return render_template("index.html")

    event_list = Event.query.all()
        
    return render_template("/divisions/add_divisions.html", event_list = event_list)

        