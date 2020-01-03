from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (
    StringField, SubmitField,
    TextAreaField, FloatField, IntegerField, 
    MultipleFileField
    )
from wtforms.fields.html5 import DateField
from wtforms.validators import (
    ValidationError, DataRequired, 
    EqualTo, optional
    )


class StatisticsForm(FlaskForm):
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
