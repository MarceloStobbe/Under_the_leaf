from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class AuthForm(FlaskForm):
    name = StringField('Name')
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4)])
    submit = SubmitField('Submit')

class QuestionForm(FlaskForm):
    content = TextAreaField('Content', validators=[DataRequired(), Length(min=5)])
    submit = SubmitField('Post Question')

class CommentForm(FlaskForm):
    content = TextAreaField('Content', validators=[DataRequired(), Length(min=2)])
    submit = SubmitField('Reply')