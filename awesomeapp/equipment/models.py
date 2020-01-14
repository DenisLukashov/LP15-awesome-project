from flask_login import current_user

from awesomeapp.extensions import db


class EquipmentType(db.Model):
    __tablename__ = 'equipment_types'
    id = db.Column(db.Integer, primary_key=True)
    
    type_name = db.Column(db.String(32), unique=True)
    
      
class Equipment(db.Model):
    __tablename__ = 'equipment'
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        index=True
    )
    user = db.relationship('User', backref='equipment')

    type_id = db.Column(
        db.Integer,
        db.ForeignKey('equipment_types.id', ondelete='CASCADE'),
        index=True
    )
    type = db.relationship('EquipmentType', backref='equipment')

    name = db.Column(db.String(128), nullable=False)
    avatar = db.Column(db.String(128))
    about = db.Column(db.Text)

    @classmethod
    def get_all_user_equipment(cls):
        return Equipment.query.filter(Equipment.user_id == current_user.id
                                      ).all()

    @classmethod
    def get_last_equipment(cls):
        return Equipment.query.filter(Equipment.user_id == current_user.id
                                      ).order_by(Equipment.id.desc()).first()

    @classmethod
    def get_equipment_by_id(cls, id):
        return Equipment.query.get(id)
