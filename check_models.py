from models import *
from sqlalchemy.orm import sessionmaker
from db_credentials import *

engine = create_engine(DATABASE_CONNECTION)
Session = sessionmaker(bind=engine)
session = Session()

user1 = User(userId=1, username='user_20', password='hgp880d', role=2)
user2 = User(userId=2, username='user_21', password='hgp881d', role=1)

city1 = City(cityId=1, cityname='Lviv')

ad1 = Ad(title='empty', content='empty', from_user=user1, from_city=city1)
ad2 = Ad(title='empty', content='empty', from_user=user2, from_city=city1)

session.add(user1)
session.add(user2)
session.commit()

session.add(city1)
session.commit()

session.add(ad1)
session.add(ad2)
session.commit()
