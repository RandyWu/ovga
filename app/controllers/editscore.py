from app import app
from flask import Flask, session,render_template,request,redirect, url_for
from app.model.model import db,Event,Score,Venue,PlayerDivision,Hole,Player

#TODO: The input fields where the player strokes are need validation to accept valid inputs
#TODO: The submit button needs to have validation as well

@app.route('/editscore', methods=['POST', 'GET'])
def editscore():
    session_event = int(session['edit_score_event'])    
    selected_event = Event.query.filter_by(EventId=session_event).first()

    if session['edit_score_event']:
        if request.method == 'POST' and request.form["submit"]:
            form = request.form
            for key,value in form.items():
                if 'score' in key:
                    #cut 'score' out of the key to leave the score id
                    id = key[5:]
                    new_score = int(value)
                    update_score = Score.query.filter_by(ScoreId=id).first()

                    update_score.Strokes = value
                    db.session.commit()

        selected_venue = Venue.query.filter_by(VenueId=selected_event.Venue_Id).first()
        
        event_name = selected_event.Name
        event_address = selected_event.Address
        event_venue = selected_venue.Name
        event_groups = PlayerDivision.query.filter_by(Event_Id=session_event).all()
        distinct_groups = []
        course_holes = Hole.query.filter_by(CourseID=selected_event.CourseID)

        for group in event_groups:
            distinct_groups.append(group.Division_Id)
        distinct_groups = list(set(distinct_groups))
        distinct_groups.sort()

    return render_template("editscore.html",
        event_name=event_name,
        event_address=event_address,
        event_venue=event_venue,
        event_groups=distinct_groups,
        course_holes=course_holes,
        event=selected_event
    )

@app.route('/editscore/getscore', methods=['POST', 'GET'])
def getscore():
    session_event = int(session['edit_score_event'])
    selected_group = request.form.get('group')
    selected_hole = request.form.get('hole')

    players = PlayerDivision.query.filter_by(Division_Id=selected_group, Event_Id=session_event).all()
    player_names = []
    score_list = []
    id_list = []
    for player in players:
        name = Player.query.filter_by(PlayerId=player.Player_Id).first()
        name = name.Name

        score = Score.query.filter_by(EventID=session_event,HoleID=selected_hole,PlayerID=player.Player_Id).first()
        score_id = score.ScoreId
        score = score.Strokes

        player_names.append(name)
        id_list.append(score_id)
        score_list.append(score)

    hole_par = Hole.query.filter_by(HoleID=selected_hole).first()
    hole_par = hole_par.Par

    return render_template('populate_scores.html',player_list=players,player_names=player_names,par=hole_par,stroke_list=score_list,ID=id_list)
