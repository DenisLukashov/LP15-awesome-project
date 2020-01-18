import imghdr
import os
from datetime import datetime

from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user

from awesomeapp.extensions import db
from config import Config
from awesomeapp.statistics.forms import StatisticsForm, StatisticsMenuForm
from awesomeapp.statistics.models import Stats, Story, Image
from awesomeapp.equipment.models import Equipment, EquipmentType
from awesomeapp.utils import get_redirect_target
from awesomeapp.statistics.utils import (
    convert_to_meter,
    convert_to_seconds,
    convert_time_to_user_view,
    statistics_field,
    calculate_parameter,
    avg_parameter)



blueprint = Blueprint('statistics', __name__,
                      template_folder='templates', url_prefix='/stats')


@blueprint.route('/delet/<int:id>')
def delet(id):
    db.session.delete(Equipment.get_by_id(id))
    db.session.commit()
    return redirect(url_for('dev.start_page'))


@blueprint.route('/menu/<int:id>', methods=['GET', 'POST'])
@login_required
def menu(id):
    form = StatisticsMenuForm()
    return render_template(
        'statistics/menu.html',
        form=form,
        title='Меню инвентаря',
        equipment_by_id=Equipment.get_by_id(id),
        all_equipment=Equipment.get_all(current_user.id)
        )


@blueprint.route('/view/<int:id>', methods=['GET', 'POST'])
@login_required
def view(id):
    form = StatisticsMenuForm()
    if form.validate_on_submit():
        datefrom = form.datefrom.data
        dateto = form.dateto.data

        matched_stats = Stats.query.filter(Stats.equipment_id == id).filter(
            datefrom <= Stats.date).filter(dateto >= Stats.date).all()

        total_distance = calculate_parameter('distance', matched_stats,
                                             'sum')/1000
        total_excercise_time = convert_time_to_user_view(
            calculate_parameter('time', matched_stats, 'sum'))
        total_work_time = convert_time_to_user_view(
            calculate_parameter('total_time', matched_stats, 'sum'))
        total_steps = calculate_parameter('steps', matched_stats, 'sum')
        total_up_altitude = calculate_parameter('total_up_altitude',
                                                matched_stats, 'sum')
        total_down_altitude = calculate_parameter('total_down_altitude',
                                                  matched_stats, 'sum')

        max_speed = calculate_parameter('max_speed', matched_stats, 'max')/1000
        max_cadence = calculate_parameter('max_cadence', matched_stats, 'max')
        max_heart_rate = calculate_parameter('max_heart_rate', matched_stats,
                                             'max')
        max_temperature = calculate_parameter('max_temperature', matched_stats,
                                              'max')
        max_altitude = calculate_parameter('max_altitude', matched_stats,
                                           'max')

        avg_cadence = avg_parameter('avg_cadence', 'time', matched_stats)
        avg_heart_rate = avg_parameter('avg_heart_rate', 'time', matched_stats)
        
        min_temperature = calculate_parameter('min_temperature', matched_stats,
                                              'min')
        min_altitude = calculate_parameter('min_altitude', matched_stats,
                                           'min')
    return render_template(
        'statistics/stats_view.html',
        datefrom=datefrom,
        dateto=dateto,
        distance=total_distance,
        time=total_excercise_time,
        total_up_altitude=total_up_altitude,
        total_time=total_work_time,
        total_down_altitude=total_down_altitude,
        steps=total_steps,
        max_speed=max_speed,
        max_cadence=max_cadence,
        max_heart_rate=max_heart_rate,
        max_temperature=max_temperature,
        max_altitude=max_altitude,
        min_altitude=min_altitude,
        min_temperature=min_temperature,
        avg_cadence=avg_cadence,
        avg_heart_rate=avg_heart_rate,
        form=form,
        title='Просмотр статистики',
        equipment_by_id=Equipment.get_by_id(id),
        all_equipment=Equipment.get_all(current_user.id)
        )


@blueprint.route('/add/<int:id>', methods=['GET', 'POST'])
@login_required
def add(id):
    form = StatisticsForm()
    if form.validate_on_submit():
        stats = Stats(
            equipment_id=id,
            date=form.date.data,
            distance=convert_to_meter(form.distance.data),
            time=convert_to_seconds(form.time.data),
            total_time=convert_to_seconds(form.total_time.data),
            max_speed=convert_to_meter(form.max_speed.data),
            steps=form.steps.data,
            avg_cadence=form.avg_cadence.data,
            max_cadence=form.max_cadence.data,
            avg_heart_rate=form.avg_heart_rate.data,
            max_heart_rate=form.max_heart_rate.data,
            max_temperature=form.max_temperature.data,
            min_temperature=form.min_temperature.data,
            start_altitude=form.start_altitude.data,
            total_up_altitude=form.total_up_altitude.data,
            total_down_altitude=form.total_down_altitude.data,
            min_altitude=form.min_altitude.data,
            max_altitude=form.max_altitude.data,
        )
        db.session.add(stats)
        db.session.commit()

        story = Story(
            text=form.story.data,
            stats_id=stats.id
        )
        db.session.add(story)
        db.session.commit()

        stats.story_id = story.id
        db.session.add(stats)
        db.session.commit()

        images = form.photo.data
        if images[0].mimetype != 'application/octet-stream':
            for image in images:
                img = Image(story_id=story.id)
                db.session.add(img)
                db.session.commit()
                file_type = imghdr.what(image)
                filename = f'{img.id}.{file_type}'
                image.save(os.path.join(Config.GLOBAL_PATH,
                                        Config.STORY_IMAGE_PATH, filename))
                img.src = os.path.join(Config.STORY_IMAGE_PATH, filename)
                db.session.add(img)
                db.session.commit()
        return redirect(url_for('statistics.menu', id=id))
    fields = statistics_field(Equipment.get_by_id(id).type_id)
    return render_template('statistics/stats.html',
                           title='Ввод данных',
                           form=form,
                           all_equipment=Equipment.get_all(current_user.id),
                           equipment_by_id=Equipment.get_by_id(id),
                           fields=fields
                           )
