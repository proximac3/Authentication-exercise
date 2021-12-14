
from models import db, User
from app import app
 
# Create all tables
db.drop_all()
db.create_all()

#add User 
sophon = User(username='protector', password='3bp', email='bmp@trisolar.com', first_name='sophon', last_name='dasha')

db.session.add(sophon)

db.session.commit()