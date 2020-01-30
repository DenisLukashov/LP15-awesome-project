from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (
    BooleanField,
    PasswordField,
    StringField,
    SubmitField,
    TextAreaField
)
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Length,
    ValidationError
)

from awesomeapp.user.models import User


class LoginForm(FlaskForm):
    email = StringField(
        'Email',
        validators=[DataRequired(), Email()],
        render_kw={
            'size': 64,
            'class': 'form-control',
            'placeholder': 'Адрес электронной почты',
        }
    )

    password = PasswordField(
        'Пароль',
        validators=[DataRequired()],
        render_kw={
            'class': 'form-control',
            'placeholder': 'Пароль'
        }
    )

    remember_me = BooleanField(
        'Запомнить меня',
        render_kw={
            'class': 'form-check-input'
        }
    )

    submit = SubmitField(
        'Войти',
        render_kw={
            'class': 'btn btn-lg btn-primary btn-block'
        }
    )

    def validate(self):
        valid = super().validate()
        if not valid:
            return False

        user = User.query.filter_by(email=self.email.data).first()

        if not user:
            self.email.errors.append(
                'Не правильные почта или пароль, или то и то:)')
            return False

        if not user.check_password(self.password.data):
            self.email.errors.append(
                'Не правильные почта или пароль, или то и то:)')
            return False

        return True


class RegistrationForm(FlaskForm):
    first_name = StringField(
        'Имя',
        validators=[Length(max=64)],
        render_kw={
            'class': 'form-control',
            'placeholder': 'Имя'
        }
    )

    second_name = StringField(
        'Фамилия',
        validators=[Length(max=64)],
        render_kw={
            'class': 'form-control',
            'placeholder': 'Фамилия'
        }
    )

    email = StringField(
        'Адрес электронной почты',
        validators=[DataRequired(), Email(), Length(max=64)],
        render_kw={
            'class': 'form-control',
            'placeholder': 'Адрес электронной почты',
            'type': 'email'
        }
    )

    password = PasswordField(
        'Пароль',
        validators=[DataRequired()],
        render_kw={
            'class': 'form-control',
            'placeholder': 'Пароль',
            'type': 'password'
        }
    )

    password2 = PasswordField(
        'Повторить пароль',
        validators=[DataRequired(), EqualTo('password')],
        render_kw={
            'class': 'form-control',
            'placeholder': 'Повторите пароль',
            'type': 'password',
        }
    )

    about_me = TextAreaField(
        'Обо мне',
        render_kw={
            'class': 'form-control',
            'placeholder': 'Обо мне',
            'rows': '3'
        }
    )

    avatar = FileField(
        'Выбрать фото',
        validators=[FileAllowed(
            ['jpg', 'jpeg', 'gif', 'png'],
            'Только изображения!')],
        render_kw={
            'class': 'form-control-file',
            'type': 'file'
        }
    )

    submit = SubmitField(
        'Зарегистрироваться',
        render_kw={
            'class': 'btn btn-lg btn-primary btn-block '
        }
    )

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError(
                'Этот адрес электронной почты уже зарегистрирован'
            )
