from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user

class UpdateProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    name = StringField('Name', validators=[Length(min=2, max=100)])
    bio = TextAreaField('Bio', validators=[Length(max=500)])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    email = StringField('Email', render_kw={'readonly': True})  # Prevent editing
    submit = SubmitField('Update')

