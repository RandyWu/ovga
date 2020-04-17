from app import app
from flask import Flask,session,render_template,request,redirect,url_for
from app.model.model import *
from flask_login import current_user, login_user

@app.route('/scores/<event_id>')
def scores(event_id):
    event = Event.query.filter_by(EventId=event_id).first()
    course_id = event.CourseID
    event_name = event.Name
    event_address = event.Address
    venue_name = Venue.query.filter_by(VenueId=event.Venue_Id).first()
    venue_name = venue_name.Name

    all_players = PlayerDivision.query.filter_by(Event_Id=event_id).all()
    all_divisions = Division.query.filter_by(EventID=event_id).distinct().all()

    page_info = {}
    score_totals = {}
    for divisions in all_divisions:
        page_info[divisions.DivisionID] = {}

    for player in all_players:
        player_name = Player.query.filter_by(PlayerId=player.Player_Id).first()
        player_name = player_name.Name
        player_scores = Score.query.filter_by(PlayerID=player.Player_Id, EventID=event_id).all()

        page_info[player.Division_Id].update({player.Player_Id:{}})
        page_info[player.Division_Id][player.Player_Id].update({"Name":player_name})
        page_info[player.Division_Id][player.Player_Id].update({"Scores":{}})

        for score in player_scores:
            page_info[player.Division_Id][player.Player_Id]["Scores"].update({score.HoleID : score.Strokes})

        score_totals.update({player.Player_Id : sum(page_info[player.Division_Id][player.Player_Id]["Scores"].values())})

    holes = Hole.query.filter_by(CourseID=course_id).order_by(Hole.Hole_Num.asc())
    
    num_of_holes = 0
    for entry in holes:
        num_of_holes += 1

    par_list = []
    for hole in range(0,num_of_holes):
        par_list.append(holes[hole].Par)
    par_total = sum(par_list)

    # TODO: Player Results
    # score_list = []
    # for hole in range(num_of_holes):
    #     score_list.append(player_scores[hole].Strokes)
    # player_total_score = sum(score_list)

    return render_template(
        "scores.html", 
        event_name = event_name,
        event_address = event_address,
        venue_name = venue_name,
        holes = holes, 
        page_info = page_info, 
        num_of_holes = num_of_holes, 
        par_list = par_list, 
        par_total = par_total,
        score_totals = score_totals
    )