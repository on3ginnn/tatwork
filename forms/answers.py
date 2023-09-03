from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FieldList, RadioField, FormField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired


class TestAnswersForm(FlaskForm):
    test_answers = FieldList(RadioField('Вопрос', choices=[('Вариант ответа 1', 'Вариант ответа 1'),
                                                           ('Вариант ответа 2', 'Вариант ответа 2'),
                                                           ('Вариант ответа 3', 'Вариант ответа 3'),
                                                           ('Вариант ответа 4', 'Вариант ответа 4')],
                                        validators=[DataRequired()]), min_entries=0)

    submit = SubmitField('Сохранить')
