from app import app
from app.model.model import *
from flask import Flask, render_template

@app.route('/scores')
def scores():
    event_id = 1
    course_id = 1

    all_players = PlayerDivision.query.filter_by(Event_Id=event_id).all()
    all_divisions = Division.query.filter_by(EventID=event_id).distinct().all()

    page_info = {}
    score_totals = {}
    for divisions in all_divisions:
        page_info[divisions.DivisionID] = {}
        # page_info[divisions.DivisionID].update({})

    for player in all_players:
        page_info[player.Division_Id].update({player.Player_Id:{}})
        player_scores = Score.query.filter_by(PlayerID=player.Player_Id, EventID=event_id).all()

        for score in player_scores:
            page_info[player.Division_Id][player.Player_Id].update({score.HoleID : score.Strokes})

        score_totals.update({player.Player_Id : sum(page_info[player.Division_Id][player.Player_Id].values())})
        

    # course = Course.query.filter_by(CourseID=course_id).first()

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