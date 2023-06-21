from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, SelectField, BooleanField, FileField
from wtforms.validators import DataRequired, Optional


class RegisterForm(FlaskForm):
    name = StringField('Имя', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    group = SelectField('Группа', choices=[('ИС-222б', 'ИС-222б'), ('ИС-221', 'ИС-221')])
    avatar = FileField('Аватар', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Форматы: jpg, png, jpeg')])
    submit = SubmitField('Подтвердить')


class ProfileEdit(FlaskForm):
    name = StringField('Имя', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    group = SelectField('Группа', choices=[('ИС-222б', 'ИС-222б'), ('ИС-221', 'ИС-221')], validators=[Optional()])
    avatar = FileField('Аватар', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Форматы: jpg, png, jpeg')])
    submit = SubmitField('Подтвердить')


class LoginForm(FlaskForm):
    name = StringField('Имя', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')