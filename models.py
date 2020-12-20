from sqlalchemy import Column, ForeignKey, Integer, String, MetaData, orm
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import create_engine

from db_credentials import *

engine = create_engine(DATABASE_CONNECTION)

metadata = MetaData(engine)
Base = declarative_base(metadata)


class User(Base):
    __tablename__ = 'Users'
    userId = Column(Integer, unique=True)
    username = Column(String(50), primary_key=True)
    password = Column(String(250))
    role = Column(Integer)

    '''def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role'''


class City(Base):
    __tablename__ = 'Cities'

    cityId = Column(Integer, unique=True)
    cityname = Column(String(50), primary_key=True)

    '''def __init__(self, cityId, cityname):
        self.cityId = cityId
        self.cityname = cityname'''


class Ad(Base):
    __tablename__ = 'Ads'

    adId = Column(Integer, autoincrement=True, primary_key=True)
    title = Column(String(50))
    content = Column(String(50))
    author = Column(String(50), ForeignKey('Users.username'))
    city = Column(String(50), ForeignKey('Cities.cityname'))

    from_user = orm.relationship(User, foreign_keys=[author], backref='adinf_from', lazy='joined')
    from_city = orm.relationship(City, foreign_keys=[city], backref='adinf_from', lazy='joined')

    '''def __init__(self, title, content, from_user, from_city):
        self.title = title
        self.content = content
        self.author = from_user
        self.city = from_city'''


Base.metadata.create_all(engine)
