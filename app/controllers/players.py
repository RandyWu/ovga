from app import app
from flask_login import current_user, login_user
from flask import Flask, session, render_template, request, redirect, url_for, jsonify
from app.model.model import Admin, Player, User, Event, Score, PlayerDivision, Venue, db, Course, Hole

@app.route('/players')
def players():
    return render_template("players.html")


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