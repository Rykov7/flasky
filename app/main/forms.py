from wtforms import StringField, SubmitField, TextAreaField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Regexp, ValidationError, Email
from flask_wtf import FlaskForm
from ..models import Role, User
from flask_pagedown.fields import PageDownField


class EditProfileForm(FlaskForm):
    name = StringField('Настоящее имя', validators=[Length(0, 64)])
    location = StringField('Месторасположение', validators=[Length(0, 64)])
    about_me = TextAreaField('Обо мне')
    submit = SubmitField('Отправить')


class EditProfileAdminForm(FlaskForm):
    email = StringField('Электронная почта', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    username = StringField('Имя пользователя', validators=[
        DataRequired(), Length(1, 64),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               'Имя пользователя должно состоять из букв, чисел, точек или нижних подчёркиваний')
    ])
    confirmed = BooleanField('Электронная почта подтверждена')
    role = SelectField('Роль', coerce=int)
    name = StringField('Настоящее имя', validators=[Length(0, 64)])
    location = StringField('Месторасположение', validators=[Length(0, 64)])
    about_me = TextAreaField('Обо мне')
    submit = SubmitField('Отправить')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError('Такая электронная почта уже существует.')

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError('Это имя пользователя уже занято.')


class PostForm(FlaskForm):
    body = PageDownField("О чём думаете? (можете использовать Markdown)", validators=[DataRequired()])
    submit = SubmitField('Отправить')


class CommentForm(FlaskForm):
    body = StringField('', validators=[DataRequired()])
    submit = SubmitField('Отправить')
