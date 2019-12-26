from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextField, TextAreaField, SelectField
from wtforms.validators import  ValidationError, DataRequired, Email, EqualTo, Length
from flask_wtf.file import FileField, FileAllowed

from awesomeapp.models import User, EquipmentType


class LoginForm(FlaskForm):
    email = StringField('Email', 
        validators=[DataRequired(), Email()],
        render_kw = {
        'size': 64,
        'class': 'form-control'
        }
    )
    
    password = PasswordField('Пароль',
        validators=[DataRequired()],
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


class RegistrationForm(FlaskForm):
    first_name = StringField('Имя',
        validators=[Length(max=64)], 
        render_kw={
            'class': 'form-control', 
            'placeholder': 'Имя'
        })
    
    second_name = StringField('Фамилия', 
        validators=[Length(max=64)],
        render_kw={
            'class': 'form-control', 
            'placeholder': 'Фамилия' 
        })
    
    email = StringField('Адрес электронной почты', 
        validators=[DataRequired(), Email(), Length(max=64)],
        render_kw={
            'class': 'form-control', 
            'placeholder': 'Адрес электронной почты', 
            'type': 'email'
        })
    
    password = PasswordField('Пароль', 
        validators=[DataRequired()],
        render_kw={
            'class': 'form-control', 
            'placeholder': 'Пароль', 
            'type': 'password'
        })
    
    password2 = PasswordField('Повторить пароль', 
        validators=[DataRequired(), EqualTo('password')],
        render_kw={
            'class': 'form-control',
            'placeholder': 'Повторите пароль',
            'type': 'password'
        })
    
    about_me = TextAreaField('Обо мне',
        render_kw={
            'class': 'form-control', 
            'placeholder': 'Обо мне',
            'rows': '3'
        })
    
    avatar = FileField('Выбрать файл', 
        validators=[FileAllowed(['jpg', 'jpeg', 'gif', 'png'], 'Только изображения!')],
        render_kw={
            'class': 'form-control-file',
            'type': 'file'
        })
    
    submit = SubmitField('Зарегистрироваться',
        render_kw={
            'class': 'btn btn-lg btn-primary btn-block'
        })

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Этот адрес электронной почты уже зарегистрирован')
        
        
class EquipmentForm(FlaskForm):
    name = StringField('Спорт инвентарь', 
        validators=[DataRequired()],
        render_kw={
            'size': 128,
            'class': 'form-control',  
        })
    
    type = SelectField('Вид спорта',
        validators=[DataRequired()],
        choices=[(f'{equipment_type.id}',f'{equipment_type.type_name}') for equipment_type in EquipmentType.query.all()],
        render_kw={
            'class': 'form-control',  
        })
    
    avatar = FileField('Изображение вашего инвентаря',
        validators=[FileAllowed(['jpg', 'jpeg', 'gif', 'png'], 'Только изображения!')],
        render_kw={
            'class': 'custom-file-input',  
        }    )
    
    about = TextAreaField('История связанная с инвентарем',
        render_kw={
            'placeholder': 'Не забудте подробно описать ваш инвентарь',
            'class': 'form-control',  
        })

    submit = SubmitField('Добавить',
        render_kw = {
            'class': 'btn btn-primary'
        })
