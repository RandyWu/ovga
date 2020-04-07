from app import app
from flask import Flask,session,render_template,request
from app.model.model import db, PlayerDivision,Event,Score
from flask_login import current_user, login_user

@app.route('/editplayerscore', methods=['POST', 'GET'])
def editplayerscore():
    user = current_user.UserId
    if request.method == 'POST' and request.form.get('submit'):
        selected_event = int(request.form.get('select_event'))
        
        form = request.form
        for key,value in form.items():
            if 'Hole' in key:
                score_id = int(key[4:])
                new_score = value

                update_score = Score.query.filter_by(ScoreId=score_id).first()
                update_score.Strokes = new_score
        db.session.commit()

    registered_events = Event.query.join(PlayerDivision, Event.EventId == PlayerDivision.Event_Id).filter_by(Player_Id=user).all()
    return render_template("editplayerscore.html", registered_events=registered_events)

@app.route('/editplayerscore/getplayerscores', methods=['POST', 'GET'])
def getplayerscores():
    user = current_user.UserId
    selected_event = int(request.form.get('event'))
    player_scores = Score.query.filter_by(EventID=selected_event, PlayerID=user).all()
    return render_template("getplayerscore.html", player_scores=player_scores)