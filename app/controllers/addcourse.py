from app import app
from flask import Flask, render_template, request
from app.model.model import db,Venue,Course,Hole

#TODO: Confirmation message on successful submit
#TODO: Form validation for course_name. No special characters
#TODO: Form security
#TODO: Form validation for hole_num. Numbers only, can't be 0

@app.route('/addcourse', methods=['POST','GET'])
def addcourse():
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
    return render_template("addcourse.html", venue_list=venue_list)