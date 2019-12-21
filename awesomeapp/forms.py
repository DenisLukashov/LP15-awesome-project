from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextField
from wtforms.validators import  ValidationError, DataRequired, Email, EqualTo, Length
from flask_wtf.file import FileField, FileAllowed

from .models import User


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()],
        render_kw = {
        'size': 64,
        'class': 'form-control'
        }
    )
    
    password = PasswordField('Пароль', validators=[DataRequired()],
        render_kw = {
        'class': 'form-control'
        }
    )
    
    remember_me = BooleanField('Запомнить меня',
        render_kw = {
        'class': 'form-check-input'
        }
    )
    
    submit = SubmitField('Войти',
        render_kw = {
        'class': 'btn btn-primary'
        }                    
    )
    
