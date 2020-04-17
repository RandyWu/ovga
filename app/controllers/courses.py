from app import app
from flask_login import current_user, login_user
from flask import Flask, session, render_template, jsonify, request, redirect, flash, url_for
from app.model.model import Admin, Player, User, Event, Score, PlayerDivision, Venue, db, Course, Hole

@app.route('/courses/home')
def courses_landing():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    user = User.query.filter_by(UserId=current_user.UserId).first()
    if user.Role != 'Admin':
        flash("Opps you don't have access to this page")
        return render_template("index.html")
    return render_template("/courses/courses_landing.html")

#TODO: Confirmation message on successful submit
#TODO: Form validation for course_name. No special characters
#TODO: Form security
#TODO: Form validation for hole_num. Numbers only, can't be 0

@app.route('/courses/add', methods=['POST','GET'])
def addcourse():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    user = User.query.filter_by(UserId=current_user.UserId).first()
    if user.Role != 'Admin':
        flash("Opps you don't have access to this page")
        return render_template("index.html")

    if request.method == 'POST' and request.form["submit"]:
        venue_id = int(request.form.get('venue_select'))
        course_name = request.form.get('course_name')
        hole_num = int(request.form.get('hole_num'))

        new_course = Course(VenueID=venue_id,CourseName=course_name,Num_Holes=hole_num)
        db.session.add(new_course)
        db.session.commit()

        course_id = Course.query.order_by(Course.CourseID.desc()).first()
        course_id = int(course_id.CourseID)

        for i in range(1,hole_num+1):
            new_hole = Hole(CourseID=course_id,Hole_Num=i,Par=0)
            db.session.add(new_hole)
        db.session.commit()

    venue_list = Venue.query.all()
    if len(venue_list) != 0:
        success = 'TRUE'
    else:
        success = 'FALSE'
    return render_template("/courses/addcourse.html", venue_list=venue_list, success=success)

@app.route('/courses/edit', methods=['POST', 'GET'])
def editcourses():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    user = User.query.filter_by(UserId=current_user.UserId).first()
    if user.Role != 'Admin':
        flash("Opps you don't have access to this page")
        return render_template("index.html")

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
    return render_template("/courses/editcourses.html", venue_list=venue_list)

@app.route('/courses/edit/getpar', methods=['POST', 'GET'])
def getpar():
    course_id = int(request.form.get('course'))
    course_holes = Hole.query.filter_by(CourseID=course_id).all()
    return render_template("/courses/get_par.html", course_holes=course_holes)