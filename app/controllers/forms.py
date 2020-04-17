from app import app
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators
from app.model.model import Admin, Player

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[validators.DataRequired(), validators.Email()])
    password = PasswordField('Password',  validators=[validators.DataRequired()])

    def validate_email(self, email):
        player = Player.query.filter_by(Email=email.data).first()
        if player == None:
            raise validators.ValidationError('Email not registered')
        if player.Password != self.password.data:
            raise validators.ValidationError('Incorrect Password')
