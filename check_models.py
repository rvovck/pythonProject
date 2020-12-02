from models import *


session = Session()


user = User(uid=1, username='user_20', password='hgp880d', role=2)
city = City(cid=1, name='Lviv')
ad = AD(adid=1, title='empty', content='empty', from_user=user, from_city=city)


session.add(user)
session.add(city)
session.add(ad)

session.commit()
