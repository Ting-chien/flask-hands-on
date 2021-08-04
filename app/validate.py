from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, Email, EqualTo, Regexp

class AccountForm(FlaskForm):
    firstname = StringField("First Name", validators=[InputRequired(), Length(max=20)])
    lastname = StringField("Last Name", validators=[InputRequired(), Length(max=20)])
    email = StringField("Email",validators=[InputRequired(),Email()])
    password = PasswordField("Password", validators=[
        InputRequired(), 
        Length(min=4,max=10),
        Regexp("^[0-9]*$", message="Invalid password")])
    confirm_password  = PasswordField("Confirm Password", validators=[
        InputRequired(),
        Length(min=4,max=10),
        Regexp("^[0-9]*$", message="Invalid password"),
        EqualTo('password', "Password must match")])

class LoginForm(FlaskForm):
    email = StringField("Email",validators=[InputRequired(),Email()])
    password = PasswordField("Password", validators=[
        InputRequired(), 
        Length(min=4,max=10),
        Regexp("^[0-9]*$", message="Invalid password")])