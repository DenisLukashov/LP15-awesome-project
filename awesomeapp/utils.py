from urllib.parse import urlparse, urljoin
from flask import request
from flask_login import current_user

from awesomeapp.equipment.models import Equipment


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


def get_redirect_target():
    for target in request.values.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return target


def get_equips():
    return Equipment.query.filter(Equipment.user_id == current_user.id).all()

def get_last_qeuip():
    return Equipment.query.filter(Equipment.user_id == current_user.id).order_by(Equipment.id.desc()).first()

def get_equip_by_id(id):
    return Equipment.query.get(id)
