from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User


class LoginForm(FlaskForm):
    email = StringField('Электронная почта', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class RegistrationForm(FlaskForm):
    email = StringField('Электронная почта', validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField('Имя пользователя', validators=[
        DataRequired(), Length(1, 64),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               'Имя пользователя должно состоять только из букв, чисел, точек и нижних подчёркиваний.')])
    password = PasswordField('Пароль', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Подтвердите пароль', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Такая электронная почта уже зарегистрирована.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Данное имя пользователя уже используется.')