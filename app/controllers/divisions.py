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

    if request.method == 'POST' and request.form["submit"]:
        session['edit_divisions_event'] = request.form.get("event_select")
        return redirect(url_for('edit_divisions'))

    return render_template("/divisions/divisions_home.html", event_list=event_list)

@app.route('/divisions/edit')
def edit_divisions():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    user = User.query.filter_by(UserId=current_user.UserId).first()
    if user.Role != 'Admin':
        flash("Opps you don't have access to this page")
        return render_template("index.html")

    session_event = int(session['edit_divisions_event'])    
    selected_event = Event.query.filter_by(EventId=session_event).first()
    if session['edit_divisions_event']:
        # if request.method == 'POST' and request.form["submit"]:
        #     form = request.form
        #     for key,value in form.items():
        #         if 'score' in key:
        #             #cut 'score' out of the key to leave the score id
        #             id = key[5:]
        #             new_score = int(value)
        #             update_score = Score.query.filter_by(ScoreId=id).first()

        #             update_score.Strokes = value
        #             db.session.commit()

        selected_venue = Venue.query.filter_by(VenueId=selected_event.Venue_Id).first()
        
        event_name = selected_event.Name
        event_address = selected_event.Address
        event_venue = selected_venue.Name
        event_groups = PlayerDivision.query.filter_by(Event_Id=session_event, ).all()
        distinct_groups = []
        course_holes = Hole.query.filter_by(CourseID=selected_event.CourseID)

        for group in event_groups:
            distinct_groups.append(group.Division_Id)
        distinct_groups = list(set(distinct_groups))
        distinct_groups.sort()

        return render_template("/divisions/edit_divisions.html",
            event_name=event_name,
            event_address=event_address,
            event_venue=event_venue,
            event_groups=distinct_groups,
            course_holes=course_holes,
            event=session_event
        )

    
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
    
    players_list = Player.query.all()
    alert = "none"
    
    if len(players_list) != 0:
        success = 'TRUE'
    else:
        success = 'FALSE'
    
    if request.method == 'POST' and request.form['btn_save'] == 'block' and request.form['player_select'] != '-1':
        players_list = Player.query.all()  
        player_id = int(request.form['player_select'])
        player = Player.query.filter_by(PlayerId=player_id).first()
        player.Name = request.form['player_name']
        player.Password = request.form['player_passwd']
        player.Email = request.form['player_email']
        db.session.commit()
        alert = "block"
        
    return render_template("/divisions/add_divisions.html", event_list = event_list, success = success, alert = alert)

        

# @app.route('/scores/edit', methods=['POST', 'GET'])
# def editscore():
#     if not current_user.is_authenticated:
#         return redirect(url_for('login'))
#     user = User.query.filter_by(UserId=current_user.UserId).first()
#     if user.Role != 'Admin':
#         flash("Opps you don't have access to this page")
#         return render_template("index.html")
        
#     session_event = int(session['edit_score_event'])    
#     selected_event = Event.query.filter_by(EventId=session_event).first()

#     if session['edit_score_event']:
#         if request.method == 'POST' and request.form["submit"]:
#             form = request.form
#             for key,value in form.items():
#                 if 'score' in key:
#                     #cut 'score' out of the key to leave the score id
#                     id = key[5:]
#                     new_score = int(value)
#                     update_score = Score.query.filter_by(ScoreId=id).first()

#                     update_score.Strokes = value
#                     db.session.commit()

#         selected_venue = Venue.query.filter_by(VenueId=selected_event.Venue_Id).first()
        
#         event_name = selected_event.Name
#         event_address = selected_event.Address
#         event_venue = selected_venue.Name
#         event_groups = PlayerDivision.query.filter_by(Event_Id=session_event).all()
#         distinct_groups = []
#         course_holes = Hole.query.filter_by(CourseID=selected_event.CourseID)

#         for group in event_groups:
#             distinct_groups.append(group.Division_Id)
#         distinct_groups = list(set(distinct_groups))
#         distinct_groups.sort()

#     return render_template("/scores/editscore.html",
#         event_name=event_name,
#         event_address=event_address,
#         event_venue=event_venue,
#         event_groups=distinct_groups,
#         course_holes=course_holes,
#         event=session_event
#     )

# @app.route('/scores/edit/getscore', methods=['POST', 'GET'])
# def getscore():
#     session_event = int(session['edit_score_event'])
#     selected_group = request.form.get('group')
#     selected_hole = request.form.get('hole')

#     players = PlayerDivision.query.filter_by(Division_Id=selected_group, Event_Id=session_event).all()
#     player_names = []
#     score_list = []
#     id_list = []
#     for player in players:
#         name = Player.query.filter_by(PlayerId=player.Player_Id).first()
#         name = name.Name

#         score = Score.query.filter_by(EventID=session_event,HoleID=selected_hole,PlayerID=player.Player_Id).first()
#         if score:
#             score_id = score.ScoreId
#             score = score.Strokes

#             player_names.append(name)
#             id_list.append(score_id)
#             score_list.append(score)
        
#         else:
#             rawr = 1

#     hole_par = Hole.query.filter_by(HoleID=selected_hole).first()
#     hole_par = hole_par.Par

#     return render_template('populate_scores.html',player_list=players,player_names=player_names,par=hole_par,stroke_list=score_list,ID=id_list)
