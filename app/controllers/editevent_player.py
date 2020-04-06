from app import app
from flask import Flask,session,render_template,request
from app.model.model import db,Event,Player,PlayerDivision

@app.route('/editevent_player', methods=['POST', 'GET'])
def editevent_player():
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
                
                return render_template("editevent_player.html", registered_players=registered_players)

            elif action == "remove":
                removed_player = PlayerDivision.query.filter_by(Player_Id=player_id,Event_Id=selected_event).first()
                db.session.delete(removed_player)
                db.session.commit()

                registered_players = Player.query\
                    .join(PlayerDivision, Player.PlayerId==PlayerDivision.Player_Id)\
                    .filter_by(Event_Id=selected_event).all()

                return render_template("editevent_player.html", registered_players=registered_players)

    return render_template("editevent_player.html", registered_players=registered_players)

@app.route('/editevent_player/registered_users', methods=['POST', 'GET'])
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