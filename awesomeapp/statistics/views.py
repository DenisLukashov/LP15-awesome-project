from datetime import timedelta
import imghdr
import os

from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user, login_required

from awesomeapp.extensions import db
from config import Config
from .forms import StatisticsForm
from awesomeapp.statistics.models import Stats, Story, Image
from awesomeapp.equipment.models import Equipment
from awesomeapp.statistics.utils import convert_to_meter, convert_to_seconds

blueprint = Blueprint('statistics', __name__)


@blueprint.route('/stats', methods=['GET', 'POST']) 
@login_required
def statistics():
    form = StatisticsForm()
    if form.validate_on_submit():
        stats = Stats(
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
                image.save(os.path.join(Config.GLOBAL_PATH, Config.STORY_IMAGE_PATH, filename))
                img.src = os.path.join(Config.STORY_IMAGE_PATH, filename)
                db.session.add(img)
                db.session.commit()
    return render_template('statistics/stats.html', title='Ввод данных', form=form)