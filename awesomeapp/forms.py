from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (
    StringField, PasswordField, BooleanField, SubmitField,
    TextField, TextAreaField, FloatField, IntegerField, 
    MultipleFileField, SelectField
    )
from wtforms.fields.html5 import DateField
from wtforms.validators import (
    ValidationError, DataRequired, Email, 
    EqualTo, Length, optional
    )

from awesomeapp.models import User, EquipmentType


class LoginForm(FlaskForm):
    email = StringField('Email', 
        validators=[DataRequired(), Email()],
        render_kw = {
        'size': 64,
        'class': 'form-control',
        'placeholder': 'Адрес электронной почты'
        }
    )
    
    password = PasswordField('Пароль',
        validators=[DataRequired()],
        render_kw = {
        'class': 'form-control',
        'placeholder': 'Пароль'
        }
    )
    
    remember_me = BooleanField('Запомнить меня',
        render_kw = {
        'class': 'form-check-input'
        }
    )
    
    submit = SubmitField('Войти',
        render_kw = {
        'class': 'btn btn-lg btn-primary btn-block'
        }                    
    )


class RegistrationForm(FlaskForm):
    first_name = StringField('Имя',
        validators=[Length(max=64)], 
        render_kw={
            'class': 'form-control', 
            'placeholder': 'Имя'
        }
    )

    second_name = StringField('Фамилия', 
        validators=[Length(max=64)],
        render_kw={
            'class': 'form-control', 
            'placeholder': 'Фамилия' 
        }
    )

    email = StringField('Адрес электронной почты', 
        validators=[DataRequired(), Email(), Length(max=64)],
        render_kw={
            'class': 'form-control', 
            'placeholder': 'Адрес электронной почты', 
            'type': 'email'
        }
    )

    password = PasswordField('Пароль', 
        validators=[DataRequired()],
        render_kw={
            'class': 'form-control', 
            'placeholder': 'Пароль', 
            'type': 'password'
        }
    )

    password2 = PasswordField('Повторить пароль', 
        validators=[DataRequired(), EqualTo('password')],
        render_kw={
            'class': 'form-control',
            'placeholder': 'Повторите пароль',
            'type': 'password',
        }
    )

    about_me = TextAreaField('Обо мне',
        render_kw={
            'class': 'form-control', 
            'placeholder': 'Обо мне',
            'rows': '3'
        }
    )

    avatar = FileField('Выбрать файл', 
        validators=[FileAllowed(['jpg', 'jpeg', 'gif', 'png'], 'Только изображения!')],
        render_kw={
            'class': 'form-control-file',
            'type': 'file'
        }
    )

    submit = SubmitField('Зарегистрироваться',
        render_kw={
            'class': 'btn btn-lg btn-primary btn-block '
        }
    )

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
        }
    )
    
    type = SelectField('Вид спорта',
        validators=[DataRequired()],
        # choices=[(f'{equipment_type.id}',f'{equipment_type.type_name}') for equipment_type in EquipmentType.query.all()],
        choices = [('1', 'stub')]
        render_kw={
            'class': 'form-control',  
        }
    )
    
    avatar = FileField('Изображение вашего инвентаря',
        validators=[FileAllowed(['jpg', 'jpeg', 'gif', 'png'], 'Только изображения!')],
        render_kw={
            'class': 'custom-file-input',  
        }
    )
    
    about = TextAreaField('История связанная с инвентарем',
        render_kw={
            'placeholder': 'Не забудте подробно описать ваш инвентарь',
            'class': 'form-control',  
        }
    )

    submit = SubmitField('Сохранить',
        render_kw={
            'class': 'btn btn-lg btn-primary btn-block'
        }
    )


class Statistics(FlaskForm):
    date = DateField('Дата',
        validators=[DataRequired()],
        render_kw={
            'class': 'form-control',
        }
    )

    distance = FloatField('Пройденное расстояние',
        validators=[optional()],
        render_kw={
            'class': 'form-control',
            'onchange': "this.value = this.value.replace(',', '.')"
        }
    )

    time = StringField('Время упражнения',
        render_kw={
            'class': 'form-control',
            'placeholder': 'чч:мм:сс',
        }
    )

    total_time = StringField('Общее время тренировки',
        render_kw={
            'class': 'form-control',
            'placeholder': 'чч:мм:сс'
        }
    )

    max_speed = FloatField('Максимальная скорость',
        validators=[optional()],
        render_kw={
            'class': 'form-control',
            'onchange': "this.value = this.value.replace(',', '.')"
        }
    )

    steps = IntegerField('Количество шагов',
        validators=[optional()],
        render_kw={
            'class': 'form-control',
        }
    )

    avg_cadence = IntegerField('Средний каденс',
        validators=[optional()],
        render_kw={
            'class': 'form-control',
        }
    )
    max_cadence = IntegerField('Максимальный каденс',
        validators=[optional()],
        render_kw={
            'class': 'form-control',
        }
    )

    avg_heart_rate = IntegerField('Средний пульс',
        validators=[optional()],
        render_kw={
            'class': 'form-control',
        }
    )

    max_heart_rate = IntegerField('Максимальный пульс',
        validators=[optional()],
        render_kw={
            'class': 'form-control',
        }
    )
    
    max_temperature = FloatField('Максимальная температура',
        validators=[optional()],
        render_kw={
            'class': 'form-control',
            'onchange': "this.value = this.value.replace(',', '.')"
        }
    )

    min_temperature = FloatField('Минимальная температура',
        validators=[optional()],
        render_kw={
            'class': 'form-control',
            'onchange': "this.value = this.value.replace(',', '.')"
        }
    )
    
    start_altitude = IntegerField('Высота начальной точки',
        validators=[optional()],
        render_kw={
            'class': 'form-control',
        }
    )

    total_up_altitude = IntegerField('Суммарный подъём',
        validators=[optional()],
        render_kw={
            'class': 'form-control',
        }
    )

    total_down_altitude = IntegerField('Суммарный спуск',
        validators=[optional()],
        render_kw={
            'class': 'form-control',
        }
    )
    min_altitude = IntegerField('Минимальная высота',
        validators=[optional()],
        render_kw={
            'class': 'form-control',
        }
    )

    max_altitude = IntegerField('Максимальная высота',
        validators=[optional()],
        render_kw={
            'class': 'form-control',
        }
    )

    story = TextAreaField('О тренеровки',
        render_kw={
            'class': 'form-control',
        }
    )

    photo = MultipleFileField('Фотографии',
        validators=[FileAllowed(['jpg', 'jpeg', 'gif', 'png'], 'Только изображения!')],
        render_kw={
            'class': 'form-control-file',
            'type': 'file'
        }
    )
    
    submit = SubmitField('Сохранить',
        render_kw={
            'class': 'btn btn-lg btn-primary btn-block'
        }
    )
