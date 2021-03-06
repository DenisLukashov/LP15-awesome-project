from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (
    SelectField,
    StringField,
    SubmitField,
    TextAreaField
)
from wtforms.validators import DataRequired


class EquipmentForm(FlaskForm):
    name = StringField(
        'Спорт инвентарь',
        validators=[DataRequired()],
        render_kw={
            'placeholder': 'Название спорта или модель инвентаря',
            'size': 128,
            'class': 'form-control',
        }
    )

    type = SelectField(
        'Вид спорта',
        validators=[DataRequired()],
        choices=[],
        render_kw={
            'placeholder': 'Тип спорта',
            'class': 'form-control',
        }
    )

    avatar = FileField(
        'Изображение',
        validators=[FileAllowed(
            ['jpg', 'jpeg', 'gif', 'png'],
            'Только изображения!')],
        render_kw={
            'class': 'form-control-file',
            'type': 'file'
        }
    )

    about = TextAreaField(
        'История связанная с инвентарем',
        render_kw={
            'placeholder': 'Не забудьте подробно описать Ваш инвентарь',
            'class': 'form-control'
        }
    )

    submit = SubmitField(
        'Сохранить',
        render_kw={
            'class': 'btn btn-lg btn-primary btn-block'
        }
    )
