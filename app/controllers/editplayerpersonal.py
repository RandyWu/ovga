from app import app
from flask import Flask,session,render_template,request
from app.model.model import db, Player

# TODO: Confirmation message shows when successfully sent
@app.route('/editplayerpersonal', methods=['POST', 'GET'])
def editplayerpersonal():
    #Change player_id to logged in user from session in the future
    player_id = 3

    if request.method == 'POST' and request.form['submit']:
        player_name = request.form.get('player_name')
        player_email = request.form.get('player_email')
        player_passwd = request.form.get('player_email')

        player = Player.query.filter_by(PlayerId=player_id).first()
        player.Name = player_name
        player.Email = player_email
        #TODO : encrypt with sha1
        player.Password = player_passwd

        db.session.commit()

    player = Player.query.filter_by(PlayerId=player_id).first()
    return render_template("editplayerpersonal.html",player=player)