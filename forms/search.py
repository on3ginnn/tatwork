from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, SelectField, BooleanField, FileField
from wtforms.validators import DataRequired, Optional


class SearchForm(FlaskForm):
    searchField = StringField('Поиск...', validators=[DataRequired()])
    submit = SubmitField('Искать')