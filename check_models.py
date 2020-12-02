from models import *


session = Session()


user = User(uid=1, username='user_20', password='hgp880d', role=2)
user2 = User(uid=2, username='user_21', password='hgp880d', role=2)
city = City(cid=1, name='Lviv')
ad = AD(adid=1, title='empty', content='empty', from_user=user, from_city=city)
ad1 = AD(adid=2, title='empty', content='empty', from_user=user2, from_city=city)
ad2 = AD(adid=3, title='empty', content='empty', from_user=user2, from_city=city)


session.add(user)
session.add(user2)
session.add(city)
session.add(ad)
session.add(ad1)
session.add(ad2)

session.commit()
