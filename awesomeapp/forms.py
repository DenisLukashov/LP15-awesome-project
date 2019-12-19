from awesomeapp.models import User
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length


class RegistrationForm(FlaskForm):
    first_name = StringField('Имя', validators=[Length(max=64)])
    second_name = StringField('Фамилия', validators=[Length(max=64)])
    email = StringField('Адрес электронной почты', validators=[DataRequired(), Email(), Length(max=64)])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password2 = PasswordField(
        'Повторить пароль', validators=[DataRequired(), EqualTo('password')])
    about_me = TextAreaField('Обо мне')
    avatar = FileField('Выбьрать файл', validators=[FileAllowed(
        ['jpg', 'jpeg', 'gif', 'png'], 'Только изображения!')]
    )
    submit = SubmitField('Зарегистрироваться')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Этот адрес электронной почты уже зарегистрирован')
