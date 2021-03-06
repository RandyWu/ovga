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

@app.route('/divisions/edit', methods=['POST','GET'])
def edit_divisions():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    user = User.query.filter_by(UserId=current_user.UserId).first()
    if user.Role != 'Admin':
        flash("Opps you don't have access to this page")
        return render_template("index.html")

    event_list = Event.query.all()

    if session['selected_event']:
        selected_event = int(session['selected_event'])

        event = Event.query.filter_by(EventId=selected_event).first()
        venue_list = Venue.query.all()
        event_course = event.CourseID
        event_venue = event.Venue_Id
        course_list = Course.query.filter_by(VenueID=event_venue).all()

        event_name = event.Name
        event_date = event.Date

        event_groups = Division.query.filter_by(EventID=selected_event).distinct().all()

        if request.method == 'POST' and request.form.get('submit') == 'submit':
            group = request.form.get("div_group")
            div = Division.query.filter_by(DivisionID=group).first()
            div.Division = request.form.get("Name")
            db.session.commit()

            return render_template(
                "/divisions/divisions_home.html",
                event_groups=event_groups,
                event_list = event_list,
                )
        
    return render_template(
        "/divisions/edit_divisions.html", 
        event_groups=event_groups,
        event_name=event_name, 
        event_date=event_date,
        )

@app.route('/divisions/add', methods=['POST', 'GET'])
def add_divisions():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    user = User.query.filter_by(UserId=current_user.UserId).first()
    if user.Role != 'Admin':
        flash("Opps you don't have access to this page")
        return render_template("index.html")

    if session['selected_event']:
        selected_event = int(session['selected_event'])
        event = Event.query.filter_by(EventId=selected_event).first()
        current_divisions = Division.query.filter_by(EventID=selected_event).distinct().all()
        alert = "none"

        if request.method == 'POST' and request.form["submit"]:
            action = request.form.get('action')
            rawr = request.form

            if action == "add":
                division_name = request.form.get('name')
                new_division = Division(Division=division_name,EventID=selected_event)
                db.session.add(new_division)
                db.session.commit()

                current_divisions = Division.query.filter_by(EventID=selected_event).distinct().all()
                alert = "block"
                return render_template("/divisions/add_divisions.html", current_divisions=current_divisions,alert=alert)

            elif action == "remove":
                division_id = request.form.get('division')

                removed_division = Division.query.filter_by(DivisionID=division_id).all()
                player_division = PlayerDivision.query.filter_by(Division_Id=division_id,Event_Id=selected_event).all()
                if player_division:
                    for pd in player_division:
                        removed_score = Score.query.filter_by(PlayerID=pd.Player_Id,EventID=selected_event).all()
                        db.session.delete(removed_score)
                    db.session.delete(player_division)
                
                if removed_division:
                    for division in removed_division:
                        db.session.delete(division)
                db.session.commit()
                
                current_divisions = Division.query.filter_by(EventID=selected_event).distinct().all()
                alert = "block"
                return render_template("/divisions/add_divisions.html", current_divisions=current_divisions,alert=alert)
        
    return render_template("/divisions/add_divisions.html", current_divisions=current_divisions,alert=alert)


        