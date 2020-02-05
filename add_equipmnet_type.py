from awesomeapp import app
with app.app_context():
  from awesomeapp.equipment.models import EquipmentType
  from awesomeapp.extensions import db
  sports = ['Ходьба', 'Бег', 'Беговая дорожка', 'Лыжи', 'Лыжероллеры', 'Коньки/Ролики', 'Велосипед', 'Велотренажер']
  for sport in sports:
    db.session.add(EquipmentType(type_name=sport))
  db.session.commit()
