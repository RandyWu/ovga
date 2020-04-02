from app import app
from flask import Flask, render_template, request
from app.model.model import db,Venue,Hole,Course

@app.route('/editcourses', methods=['POST', 'GET'])
def editcourses():
    if request.method == 'POST':
        action = request.form.get('submit')
        if action == 'save':
            course_id = int(request.form.get('course_select'))
            course_name = request.form.get('course_name')
            course = Course.query.filter_by(CourseID=course_id).first()
            course.CourseName = course_name
            db.session.commit()

            form = request.form
            for key,value in form.items():
                if 'Hole' in key:
                    hole_id = key[4:]
                    new_par = value

                    update_hole = Hole.query.filter_by(HoleID=hole_id).first()
                    update_hole.Par = new_par
            db.session.commit()
            
        if action =='delete':
            course_id = int(request.form.get('course_select'))
            course = Course.query.filter_by(CourseID=course_id).first()
            holes = Hole.query.filter_by(CourseID=course_id).all()

            if course:
                db.session.delete(course)
            if holes:
                for hole in holes:
                    db.session.delete(hole)
            db.session.commit()

    venue_list = Venue.query.all()
    return render_template("editcourses.html", venue_list=venue_list)

@app.route('/editcourses/getpar', methods=['POST', 'GET'])
def getpar():
    course_id = int(request.form.get('course'))
    course_holes = Hole.query.filter_by(CourseID=course_id).all()
    return render_template("get_par.html", course_holes=course_holes)