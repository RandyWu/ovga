from app import app
from flask_wtf import FlaskForm
from wtforms import validators
from wtforms import StringField, PasswordField, validators
from app.model.model import Admin, Player

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[validators.DataRequired(), validators.Email()])
    password = PasswordField('Password',  validators=[validators.DataRequired()])

    def validate_email(self, email):
        admin = Admin.query.filter_by(Email=email.data).first()
        player = Player.query.filter_by(Email=email.data).first()
        if admin and player is not None:
            raise ValidationError('Email not registered')
