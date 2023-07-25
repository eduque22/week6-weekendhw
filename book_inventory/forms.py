from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email

class UserLoginForm(FlaskForm):
    username = StringField('username', validators = [DataRequired()])
    email = StringField('email', validators = [DataRequired(), Email()])
    password = PasswordField('password', validators = [DataRequired()])
    submit_button = SubmitField()


class BookForm(FlaskForm):
    title = StringField('title')
    author = StringField('author')
    cover = StringField('cover')
    genre = StringField('genre')
    release_date = IntegerField('release_date')
    submit_button = SubmitField()