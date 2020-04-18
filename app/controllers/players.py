from app import app
from flask_login import current_user, login_user
from flask import Flask, flash, session, render_template, request, redirect, url_for, jsonify
from app.model.model import Admin, Player, User, Event, Score, PlayerDivision, Venue, db, Course, Hole

@app.route('/players/home')
def players():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    user = User.query.filter_by(UserId=current_user.UserId).first()
    if user.Role != 'player':
        flash("Opps you don't have access to this page")
        return render_template("index.html")
    person = Player.query.filter_by(PlayerId=current_user.UserId).first()

    return render_template("/players/players.html", person=person)


@app.route('/players/edit', methods=['POST', 'GET'])
def editplayerinfo():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    user = User.query.filter_by(UserId=current_user.UserId).first()
    if user.Role != 'Admin':
        flash("Opps you don't have access to this page")
        return render_template("index.html")
    
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
        
    return render_template("/players/editplayerinfo.html", players_list = players_list, success = success, alert = alert)

@app.route('/players/getplayerinfo', methods=['POST', 'GET'])  
def getplayerinfo():
    if request.form['player_select'] != '-1':
        player_id = request.form['player_select']
        selected_player = Player.query.filter_by(PlayerId=player_id).first()
        player_name = selected_player.Name
        player_email = selected_player.Email
        player_passwd = selected_player.Password
        
        return jsonify({'player_name':player_name, 'player_email':player_email, 'player_passwd':player_passwd})

@app.route('/players/editscore', methods=['POST', 'GET'])
def editplayerscore():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    user = User.query.filter_by(UserId=current_user.UserId).first()
    if user.Role != 'player':
        flash("Opps you don't have access to this page")
        return render_template("index.html")
    person = Player.query.filter_by(PlayerId=current_user.UserId).first()

    user = current_user.UserId
    if request.method == 'POST' and request.form['submit']:
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
    return render_template("/players/editplayerscore.html", registered_events=registered_events,person=person)

@app.route('/players/editscore/getplayerscores', methods=['POST', 'GET'])
def getplayerscores():
    user = current_user.UserId
    selected_event = int(request.form.get('event'))
    player_scores = Score.query.filter_by(EventID=selected_event, PlayerID=user).all()
    return render_template("/players/getplayerscore.html", player_scores=player_scores)

@app.route('/players/editpersonal', methods=['POST', 'GET'])
def editplayerpersonal():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    user = User.query.filter_by(UserId=current_user.UserId).first()
    if user.Role != 'player':
        flash("Opps you don't have access to this page")
        return render_template("index.html")

    #Change player_id to logged in user from session in the future
    player_id = current_user.UserId
    alert = "none"

    if request.method == 'POST' and request.form['submit']:
        player_name = request.form.get('player_name')
        player_email = request.form.get('player_email')
        player_passwd = request.form.get('player_email')

        player = Player.query.filter_by(PlayerId=player_id).first()
        player.Name = player_name
        player.Email = player_email
        #TODO : encrypt with sha1
        player.Password = player_passwd
        alert = "block"
        db.session.commit()

    player = Player.query.filter_by(PlayerId=player_id).first()
    return render_template("/players/editplayerpersonal.html",player=player, alert=alert)

@app.route('/players/choose_event', methods = ['POST','GET'])
def choose_event():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    user = User.query.filter_by(UserId=current_user.UserId).first()
    if user.Role != 'player':
        flash("Opps you don't have access to this page")
        return render_template("index.html")

    user = current_user.UserId

    if request.method == 'POST' and request.form['submit']:
        selected_event = int(request.form.get('event_select'))
        return redirect(url_for('scores',event_id=selected_event))

    registered_events = PlayerDivision.query.filter_by(Player_Id=user).all()
    registered_players = PlayerDivision.query.filter_by(Player_Id=user).distinct().all()

    events = []
    for event in registered_events:
        e = Event.query.filter_by(EventId=event.Event_Id).first()
        event_id = e.EventId
        event_info = e.Name + " - " + e.Address 
        events.append((event_id,event_info))

    return render_template("/players/choose_event.html", events=events)