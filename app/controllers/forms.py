from flask_wtf import Form
from wtforms import validators
from wtforms.fields.html5 import EmailField

# class ContactForm(Form):
#     email = EmailField('Email address', [validators.DataRequired(), validators.Email()])

# class LoginForm(Form):
#     email = StringField('Email')
#     password = PasswordField('Password')

#     def validate(self):

#         if not Form.validate(self):
#             return False

#         if not self.email.data:
#             return False

#         if not self.password.data:
#             return False

#         return True
