from app import app
from app.model.model import *
from flask import Flask, render_template

@app.route('/scores')
def scores():
    player_scores = Score.query.filter_by(PlayerID=1).all()
    course = Course.query.filter_by(CourseID=1).first()
    holes = Hole.query.filter_by(CourseID=1).order_by(Hole.Hole_Num.asc())
    
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
            course = course, 
            num_of_holes = num_of_holes, 
            par_list = par_list, 
            par_total = par_total, 
            player_scores = player_scores,
            player_total_score = player_total_score
            )