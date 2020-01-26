from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import (
    FloatField,
    IntegerField,
    MultipleFileField,
    StringField,
    SubmitField,
    TextAreaField
)
from wtforms.fields.html5 import DateField
from wtforms.validators import (
    DataRequired,
    optional,
    ValidationError
)

from awesomeapp.statistics.models import Stats


class StatisticsMenuForm(FlaskForm):

    start_date = DateField(
        'С',
        validators=[DataRequired()],
        render_kw={'class': 'form-control'}
    )

    end_date = DateField(
        'По',
        render_kw={'class': 'form-control'},
        validators=[optional()],
    )

    submit = SubmitField(
        'Вывести статистику',
        render_kw={'class': 'btn btn-lg btn-primary btn-block'}
    )

    def validate(self):
        rv = FlaskForm.validate(self)
        if not rv:
            return False
        statistics = Stats.query.filter(
            Stats.date == self.start_date.data).all()

        if not statistics and self.end_date.data is None:
            self.start_date.errors.append(
                'В этот день вы не добавляли статистику')
            return False
        return True


class StatisticsForm(FlaskForm):

    date = DateField(
        'Дата',
        validators=[DataRequired()],
        render_kw={'class': 'form-control', 'placeholder': 'Дата'}
    )

    distance = FloatField(
        'Пройденное расстояние',
        validators=[optional()],
        render_kw={
            'class': 'form-control',
            'onchange': "this.value = this.value.replace(',', '.')",
            'placeholder': 'Пробег'}
    )

    time = StringField(
        'Время упражнения',
        render_kw={
            'class': 'form-control',
            'placeholder': 'Время упражнения чч:мм:сс'}
    )

    total_time = StringField(
        'Общее время тренировки',
        render_kw={
            'class': 'form-control',
            'placeholder': 'Общее время чч:мм:сс'}
    )

    max_speed = FloatField(
        'Максимальная скорость',
        validators=[optional()],
        render_kw={
            'class': 'form-control',
            'onchange': "this.value = this.value.replace(',', '.')",
            'placeholder': 'Макс скорость'}
    )

    steps = IntegerField(
        'Количество шагов',
        validators=[optional()],
        render_kw={
            'class': 'form-control',
            'placeholder': 'Шаги'}
    )

    avg_cadence = IntegerField(
        'Средний каденс',
        validators=[optional()],
        render_kw={
            'class': 'form-control',
            'placeholder': 'Сред каденс'}
    )

    max_cadence = IntegerField(
        'Максимальный каденс',
        validators=[optional()],
        render_kw={
            'class': 'form-control',
            'placeholder': 'Макс каденс'}
    )

    avg_heart_rate = IntegerField(
        'Средний пульс',
        validators=[optional()],
        render_kw={
            'class': 'form-control',
            'placeholder': 'Сред пульс'}
    )

    max_heart_rate = IntegerField(
        'Максимальный пульс',
        validators=[optional()],
        render_kw={
            'class': 'form-control',
            'placeholder': 'Макс пульс'}
    )

    max_temperature = FloatField(
        'Максимальная температура',
        validators=[optional()],
        render_kw={
            'class': 'form-control',
            'onchange': "this.value = this.value.replace(',', '.')",
            'placeholder': 'Макс температура'}
    )

    min_temperature = FloatField(
        'Минимальная температура',
        validators=[optional()],
        render_kw={
            'class': 'form-control',
            'onchange': "this.value = this.value.replace(',', '.')",
            'placeholder': 'Мин температура'}
    )

    start_altitude = IntegerField(
        'Высота начальной точки',
        validators=[optional()],
        render_kw={
            'class': 'form-control',
            'placeholder': 'Начальный уровень'}
    )

    total_up_altitude = IntegerField(
        'Суммарный подъём',
        validators=[optional()],
        render_kw={
            'class': 'form-control',
            'placeholder': 'Суммарный подъём'}
    )

    total_down_altitude = IntegerField(
        'Суммарный спуск',
        validators=[optional()],
        render_kw={
            'class': 'form-control',
            'placeholder': 'Суммарный спуск'}
    )

    min_altitude = IntegerField(
        'Минимальная высота',
        validators=[optional()],
        render_kw={
            'class': 'form-control',
            'placeholder': 'Мин высота'}
    )

    max_altitude = IntegerField(
        'Максимальная высота',
        validators=[optional()],
        render_kw={
            'class': 'form-control',
            'placeholder': 'Макс высота'}
    )

    story = TextAreaField(
        'О тренировке',
        render_kw={
            'class': 'form-control',
            'placeholder': 'О тренировке'
        }
    )

    photo = MultipleFileField(
        'Фотографии',
        validators=[FileAllowed(
            ['jpg', 'jpeg', 'gif', 'png'],
            'Только изображения!')],
        render_kw={
            'class': 'form-control-file',
            'type': 'file'}
    )

    submit = SubmitField(
        'Сохранить',
        render_kw={
            'class': 'btn btn-lg btn-primary btn-block'}
    )
