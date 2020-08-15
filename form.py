from flask_wtf import Form
from wtforms import TextField, SubmitField, IntegerField, StringField, TextAreaField
from wtforms.validators import DataRequired, Email, InputRequired
from wtforms.fields.html5 import EmailField
from flask import flash

 
class ContactForm(Form):
    name = StringField("Enter your name please", validators=[InputRequired()], render_kw={'placeholder':'Enter your name'})
    email = EmailField('Enter your email address', validators=[InputRequired(), Email('This field requires a valid email address')], render_kw={'placeholder':'Enter your email'})
    subject = StringField("Subject", validators=[InputRequired()], render_kw={'placeholder':'Enter subject'})
    message = TextAreaField("Message", validators=[InputRequired()], render_kw={'placeholder':'Your message'})
    send = SubmitField("Send")
