from flask_wtf import Form
from wtforms import TextField, SubmitField, IntegerField, StringField, TextAreaField
from wtforms.validators import DataRequired, Email
 
class ContactForm(Form):
    name = StringField("Enter your name please", render_kw={'placeholder':'Enter your name'})
    Email = StringField('Enter your email address', [Email(message='Not a valid email address.'), DataRequired()],
    render_kw={'placeholder':'Enter your email'})
    subject = StringField("Subject", render_kw={'placeholder':'Enter subject'})
    message = TextAreaField("Message", render_kw={'placeholder':'Your message'})
    send = SubmitField("Send")
