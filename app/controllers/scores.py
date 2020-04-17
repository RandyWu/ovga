from app import app
from flask_login import current_user, login_user
from flask import Flask,session,render_template,request,redirect,url_for
from app.model.model import *

@app.route('/scores/<event_id>')
def scores(event_id):
    event_course = Event.query.filter_by(CourseID=event_id).first()
    course_id = event_course.CourseID

    all_players = PlayerDivision.query.filter_by(Event_Id=event_id).all()
    all_divisions = Division.query.filter_by(EventID=event_id).distinct().all()

    page_info = {}
    score_totals = {}
    for divisions in all_divisions:
        page_info[divisions.DivisionID] = {}

    for player in all_players:
        page_info[player.Division_Id].update({player.Player_Id:{}})
        player_scores = Score.query.filter_by(PlayerID=player.Player_Id, EventID=event_id).all()

        for score in player_scores:
            page_info[player.Division_Id][player.Player_Id].update({score.HoleID : score.Strokes})

        score_totals.update({player.Player_Id : sum(page_info[player.Division_Id][player.Player_Id].values())})

    holes = Hole.query.filter_by(CourseID=course_id).order_by(Hole.Hole_Num.asc())
    
    num_of_holes = 0
    for entry in holes:
        num_of_holes += 1

    par_list = []
    for hole in range(0,num_of_holes):
        par_list.append(holes[hole].Par)
    par_total = sum(par_list)

    score_list = []
    for hole in range(num_of_holes):
        score_list.append(player_scores[hole].Strokes)
    player_total_score = sum(score_list)

    return render_template(
        "scores.html", 
        holes = holes, 
        page_info = page_info, 
        num_of_holes = num_of_holes, 
        par_list = par_list, 
        par_total = par_total,
        score_totals = score_totals
    )

@app.route('/scores/home', methods=['POST','GET'])
def editscores_landing():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    user = User.query.filter_by(UserId=current_user.UserId).first()
    if user.Role != 'Admin':
        flash("Opps you don't have access to this page")
        return render_template("index.html")

    event_list = Event.query.all()

    if request.method == 'POST' and request.form["submit"]:
        session['edit_score_event'] = request.form.get("event_select")
        return redirect(url_for('editscore'))
        
    return render_template("/scores/editscores_landing.html", event_list=event_list)

#TODO: The input fields where the player strokes are need validation to accept valid inputs
#TODO: The submit button needs to have validation as well

@app.route('/scores/edit', methods=['POST', 'GET'])
def editscore():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    user = User.query.filter_by(UserId=current_user.UserId).first()
    if user.Role != 'Admin':
        flash("Opps you don't have access to this page")
        return render_template("index.html")
        
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

    return render_template("/scores/editscore.html",
        event_name=event_name,
        event_address=event_address,
        event_venue=event_venue,
        event_groups=distinct_groups,
        course_holes=course_holes,
        event=selected_event
    )

@app.route('/scores/edit/getscore', methods=['POST', 'GET'])
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
