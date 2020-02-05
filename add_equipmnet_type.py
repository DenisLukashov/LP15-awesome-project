from awesomeapp import app
with app.app_context():
  from awesomeapp.equipment.models import EquipmentType
  from awesomeapp.extensions import db
  sport = ['Ходьба', 'Бег', 'Беговая дорожка', 'Лыжи', 'Лыжероллеры', 'Коньки/Ролики', 'Велосипед', 'Велотренажер']
  for i in sport:
    db.session.add(EquipmentType(type_name=i))
  db.session.commit()
