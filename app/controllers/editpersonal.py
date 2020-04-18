from app import app,login
from flask_login import current_user
from flask import Flask, session, render_template, request, redirect, url_for
from app.model.model import db, Admin, User, Player

@app.route('/admin/editpersonal', methods=['POST', 'GET'])
def editpersonal():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    user = User.query.filter_by(UserId=current_user.UserId).first()
    if user.Role != 'Admin':
        flash("Opps you don't have access to this page")
        return render_template("index.html")

    session['admin_id'] = current_user.UserId
    alert = "none"
    
    if request.method == 'POST' and request.form.get('submit') == 'submit':    
        admin_info = Player.query.filter_by(PlayerId=session['admin_id']).first()  
        admin_info.Email = request.form['my_email']
        admin_info.Password = request.form['my_passwd']
        db.session.commit()
        alert = "block"
        
    admin_info = Player.query.filter_by(PlayerId=session['admin_id']).first()
    my_id = admin_info.PlayerId
    my_email = admin_info.Email
    my_passwd = admin_info.Password
        
    return render_template("/admin/editpersonal.html", my_id=my_id, my_email=my_email, my_passwd=my_passwd, alert=alert)