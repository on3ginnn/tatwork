from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, TextAreaField, IntegerField, SelectField, FileField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired


class TopicForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    topic_lang = SelectField('Язык', choices=[('ТАТ', 'ТАТ'), ('РУС', 'РУС'), ('КИНО', 'КИНО')])
    author = StringField("Автор", validators=[DataRequired()])
    picture = FileField('Картинка', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Форматы: jpg, png, jpeg')])

    submit = SubmitField('Создать')