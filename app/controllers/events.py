from app import app, login
from datetime import date
from flask_login import current_user, login_user
from flask import Flask, session, render_template, jsonify, request, redirect, flash, url_for
from app.model.model import Admin, Player, User, Event, Score, PlayerDivision, Venue, db, Course

@app.route('/events')
def events():
    today = date.today()
    upcoming_events = (Event.query.filter(Event.Date > today)).order_by(Event.Date.desc()).limit(10).all()
    none = "There are no upcoming events"
    return render_template("/events/events.html", upcoming_events = upcoming_events, none=none)

@app.route('/events/home')
def events_landing():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    user = User.query.filter_by(UserId=current_user.UserId).first()
    if user.Role != 'Admin':
        flash("Opps you don't have access to this page")
        return render_template("index.html")
    return render_template("/events/events_landing.html")

@app.route('/events/delete', methods=['POST', 'GET'])
def delevent():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    user = User.query.filter_by(UserId=current_user.UserId).first()
    if user.Role != 'Admin':
        flash("Opps you don't have access to this page")
        return render_template("index.html")

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
                
        db.session.commit()

    event_list = Event.query.all()
    return render_template("/events/delevent.html", event_list=event_list)
    
@app.route('/events/add/get_event', methods=['POST', 'GET'])
def get_events():
    date = request.form.get("date")
    events = Event.query.filter_by(Date=date).all()

    if len(events) != 0:
        success = 'TRUE'
    else:
        success = 'FALSE'
        
    return render_template("populate_list.html", events=events, success=success)

@app.route('/events/add/get_course', methods=['POST', 'GET'])
def get_course():
    venue_id = request.form.get("venue")
    course_list = Course.query.filter_by(VenueID=venue_id).all()

    if len(course_list) != 0:
        success = 'TRUE'
    else:
        success = 'FALSE'
        
    return render_template("/events/get_courses.html", course_list=course_list, success=success)

@app.route('/events/add', methods=['POST', 'GET'])
def addevents():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    user = User.query.filter_by(UserId=current_user.UserId).first()
    if user.Role != 'Admin':
        flash("Opps you don't have access to this page")
        return render_template("index.html")

    venue_list = Venue.query.all()

    if request.method == 'POST' and request.form["submit"]:

        selected_venue = int(request.form.get("venue_list"))
        selected_course = int(request.form.get("course_list"))
        venue_address = Venue.query.filter_by(VenueId=selected_venue).first().Address
        event_name = request.form.get("event_name")
        event_date = request.form.get("selected_date")

        new_event = Event(Venue_Id=selected_venue,Name=event_name,Address=venue_address,Date=event_date,CourseID=selected_course)
        db.session.add(new_event)
        db.session.commit()

    return render_template("/events/addevents.html", venue_list = venue_list)

@app.route('/events/edit_info', methods=['POST', 'GET'])
def editevent_info():
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
                "/events/editevent_info.html",
                event_name=new_name,
                event_date=new_date,
                event_venue=new_venue,
                event_course=new_course,
                venue_list=venue_list,
                course_list=course_list)
        
    return render_template(
        "/events/editevent_info.html", 
        event_name=event_name, 
        event_date=event_date,
        event_venue=event_venue,
        event_course=event_course,
        venue_list=venue_list,
        course_list=course_list)
        
@app.route('/events/edit', methods=['POST', 'GET'])
def editevent_landing():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    user = User.query.filter_by(UserId=current_user.UserId).first()
    if user.Role != 'Admin':
        flash("Opps you don't have access to this page")
        return render_template("index.html")

    events_list = Event.query.all()

    if request.method == 'POST':
        session['selected_event'] = int(request.form.get('event_select'))

        if request.form.get('submit') == 'event':
            return redirect(url_for('editevent_info'))
        
        if request.form.get('submit') == 'player':
            return redirect(url_for('editevent_player'))

    return render_template('/events/editevent_landing.html', events_list=events_list)


@app.route('/events/edit_player', methods=['POST', 'GET'])
def editevent_player():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    user = User.query.filter_by(UserId=current_user.UserId).first()
    if user.Role != 'Admin':
        flash("Opps you don't have access to this page")
        return render_template("index.html")

    if session['selected_event']:
        selected_event = int(session['selected_event'])
        event = Event.query.filter_by(EventId=selected_event).first()

        registered_players = Player.query\
            .join(PlayerDivision, Player.PlayerId==PlayerDivision.Player_Id)\
            .filter_by(Event_Id=selected_event).all()

        if request.method == 'POST' and request.form["submit"]:
            player_id = request.form.get('player')
            action = request.form.get('action')

            if action == "add":
                new_player = PlayerDivision(Player_Id=player_id,Division_Id=1,Event_Id=selected_event)
                db.session.add(new_player)
                db.session.commit()

                registered_players = Player.query\
                    .join(PlayerDivision, Player.PlayerId==PlayerDivision.Player_Id)\
                    .filter_by(Event_Id=selected_event).all()
                
                return render_template("/events/editevent_player.html", registered_players=registered_players)

            elif action == "remove":
                removed_player = PlayerDivision.query.filter_by(Player_Id=player_id,Event_Id=selected_event).first()
                db.session.delete(removed_player)
                db.session.commit()

                registered_players = Player.query\
                    .join(PlayerDivision, Player.PlayerId==PlayerDivision.Player_Id)\
                    .filter_by(Event_Id=selected_event).all()

                return render_template("/events/editevent_player.html", registered_players=registered_players)

    return render_template("/events/editevent_player.html", registered_players=registered_players, event=event)

@app.route('/events/edit_player/registered_users', methods=['POST', 'GET'])
def get_registered():
    action = request.form.get("action")
    selected_event = int(session['selected_event'])
    if action == "add":
        # Failed subquery attempts
        # player_list = Player.query\
        #     .join(PlayerDivision, Player.PlayerId==PlayerDivision.Player_Id)\
        #     .filter((PlayerDivision.Event_Id != selected_event) | (PlayerDivision.Event_Id == None)).all()
        # subquery = PlayerDivision.query.filter(PlayerDivision.Player_Id)
        # player_list = Player.query.filter(Player.PlayerId.notin_(subquery)).all()

        player_list = Player.query.filter(
            ~PlayerDivision.query.filter(Player.PlayerId == PlayerDivision.Player_Id)
            .exists()
        ).all()
        
        if player_list:
            success = 'TRUE'
        else:
            success = 'FALSE'

    elif action == "remove":
        player_list = Player.query\
            .join(PlayerDivision, Player.PlayerId==PlayerDivision.Player_Id)\
            .filter_by(Event_Id=selected_event).all()
        if player_list:
            success = 'TRUE'
        else:
            success = 'FALSE'
    else:
        success = 'FALSE'

    return render_template("get_players.html", player_list=player_list, success=success)

# TODO: Figure out a way to add groups to events
# @app.route('/editevent_player/get_groups', methods=['POST', 'GET'])
# def get_groups():
#     action = request.form.get("action")
#     selected_event = int(session['selected_event'])

#     if action == "add":
#         groups = PlayerDivision.query.filter_by()
#     elif action == "remove":
#     else:
#         return None