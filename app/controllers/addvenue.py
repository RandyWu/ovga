from app import app
from flask import Flask,session,render_template,request
from app.model.model import db,Venue

@app.route('/addvenue', methods=['POST','GET'])
def addvenue():
    if request.method == 'POST':
        venue_name = request.form.get("venue_name")
        venue_address = request.form.get("venue_address")

        new_venue = Venue(Name=venue_name,Address=venue_address)
        db.session.add(new_venue)
        db.session.commit()
    
    return render_template("addvenue.html")