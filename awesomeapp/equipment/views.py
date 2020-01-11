import imghdr
import os

from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user, login_required

from awesomeapp.extensions import db
from config import Config
from awesomeapp.equipment.forms import EquipmentForm
from awesomeapp.equipment.models import Equipment, EquipmentType
from awesomeapp.utils import get_equips, get_equip_for_sport_zone, get_redirect_target

blueprint = Blueprint('equipment', __name__, template_folder='templates')


@blueprint.route('/equipment', methods=['GET', 'POST'])
@login_required
def equipment():
    form = EquipmentForm()
    form.type.choices = [
        (f'{equipment_type.id}', f'{equipment_type.type_name}')
        for equipment_type in EquipmentType.query.all()
    ]
    if form.validate_on_submit():
        equipment = Equipment(
            name=form.name.data,
            user_id=current_user.id,
            type_id=int(form.type.data),
            about=form.about.data
        )
        db.session.add(equipment)
        db.session.commit()
        equipment_avatar = form.avatar.data
        if equipment_avatar:
            equipment_avatar_type = imghdr.what(equipment_avatar)
            equipment_avatar_file = f'{equipment.id}.{equipment_avatar_type}'
            equipment_avatar.save(os.path.join(
                Config.GLOBAL_PATH,
                Config.EQUIPMENT_ICON_PATH,
                equipment_avatar_file)
            )
            equipment_avatar_path = os.path.join(
                Config.EQUIPMENT_ICON_PATH,
                equipment_avatar_file
            )
        else:
            equipment_avatar_path = os.path.join(
                Config.EQUIPMENT_ICON_PATH,
                Config.STOCK_ICON.get(form.type.data)
            )
        equipment.avatar = equipment_avatar_path
        db.session.commit()
        return redirect(get_redirect_target())
    
    return render_template('equipment/equipment.html', title='Инвентарь',
            form=form, equips=get_equips(), equip=get_equip_for_sport_zone())
