from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,TextAreaField
from wtforms.validators import DataRequired,Length,Email,EqualTo

class SignupForm(FlaskForm):
  username= StringField('Username',
                        validators=[DataRequired(),
                                    Length(min=1, max=20)])

  email = StringField('Email',
                      validators=[DataRequired(),
                                  Email(message='Invalid email')])

  password = PasswordField('Password',
                           validators=[
                             DataRequired(),
                             Length(min =8, max=128)
                           ])

  confirm_password= PasswordField('Confirm Password',
                                  validators=[
                                    DataRequired(),
                                    EqualTo('password',message='Password must match')
                                  ])

  submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
  email = StringField('Email',
                        validators=[DataRequired(),
                                    Email()])
  
  password = PasswordField('Password',
                             validators=[
                               DataRequired()
                             ])


  
  submit = SubmitField('Login')



class TextForm(FlaskForm):
  text = TextAreaField('Enter text', validators=[DataRequired()])
  submit = SubmitField('Analyze')
  