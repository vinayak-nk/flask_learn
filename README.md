# flask_learn
python 

from app import db

db.create_all()

from app import User, Post

user1 = User(username='vnk', email='vnk@test.com',password="password" )
print(user1.password)
db.session.add(user1)
>>> db.session.commit()

>>> User.query.all()
>>> User.query.first()
>>> User.query.filter_by(username="vnk)
>>> User.query.filter_by(username="vnk).first()

db.create_all()
db.drop_all()
