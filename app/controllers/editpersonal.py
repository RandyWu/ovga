from app import app,login
from flask_login import current_user
from flask import Flask, session, render_template, request, redirect, url_for
from app.model.model import db, Admin, User

@app.route('/editpersonal', methods=['POST', 'GET'])
def editpersonal():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    session['admin_id'] = 1
    alert = "none"
    
    if request.method == 'POST' and request.form.get('submit') == 'submit':    
        admin_info = Admin.query.filter_by(Admin_Id=session['admin_id']).first()  
        admin_info.Email = request.form['my_email']
        admin_info.Password = request.form['my_passwd']
        db.session.commit()
        alert = "block"
        
    admin_info = Admin.query.filter_by(Admin_Id=session['admin_id']).first()
    my_id = admin_info.Admin_Id
    my_email = admin_info.Email
    my_passwd = admin_info.Password
        
    return render_template("editpersonal.html", my_id=my_id, my_email=my_email, my_passwd=my_passwd, alert=alert)