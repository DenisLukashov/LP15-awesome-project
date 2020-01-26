import imghdr
import os

from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy.orm.exc import NoResultFound

from awesomeapp.extensions import db
from config import Config
from awesomeapp.statistics.forms import StatisticsForm, StatisticsMenuForm
from awesomeapp.statistics.models import Stats, Story, Image
from awesomeapp.equipment.models import Equipment
from awesomeapp.statistics.utils import (
    convert_to_meter,
    convert_to_seconds,
    get_statistics_fields,
)


blueprint = Blueprint(
    'statistics',
    __name__,
    template_folder='templates',
    url_prefix='/stats'
)


@blueprint.route('/delet/<int:id>')
def delete(id):
    equipment = Equipment.get_by_id(id)
    images_of_equipment = []

    nested_images = [statistics.story.images for statistics in equipment.stats]
    flat_images = [image for set_images in nested_images for
                   image in set_images]

    for image in flat_images:
        file = image.src.split('/')[-1]
        file_path = os.path.join(
            Config.GLOBAL_PATH, Config.STORY_IMAGE_PATH, file)
        images_of_equipment.append(file_path)

    for src in images_of_equipment:
        os.remove(src)

    db.session.delete(equipment)
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
        start_date = form.start_date.data
        end_date = form.end_date.data

        if end_date is None:
            end_date = start_date

        if start_date > end_date:
            start_date, end_date = end_date, start_date

        return render_template(
            'statistics/stats_view.html',
            start_date=start_date,
            end_date=end_date,
            story_and_images=Stats.get_story_and_images(
                    id, start_date, end_date),
            statistics=Stats.get_statistics(id, start_date, end_date),
            form=form,
            title='Просмотр статистики',
            equipment_by_id=Equipment.get_by_id(id),
            all_equipment=Equipment.get_all(current_user.id),
            histogram=Stats.histogram_data(start_date, end_date, id)
        )

    return render_template(
        'statistics/menu.html',
        form=form,
        title='Меню инвентаря',
        equipment_by_id=Equipment.get_by_id(id),
        all_equipment=Equipment.get_all(current_user.id),
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
    fields = get_statistics_fields(Equipment.get_by_id(id).type_id, form)
    return render_template(
        'statistics/stats.html',
        title='Ввод данных',
        form=form,
        all_equipment=Equipment.get_all(current_user.id),
        equipment_by_id=Equipment.get_by_id(id),
        fields=fields
    )
