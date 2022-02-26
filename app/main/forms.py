from flask_pagedown.fields import PageDownField
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class CommentForm(FlaskForm):
    nickname = StringField('Nickname')
    email = StringField('Email')
    body = PageDownField('Body', validators=[DataRequired()])
    submit = SubmitField('Submit')
