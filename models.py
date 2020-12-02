from sqlalchemy import *
from sqlalchemy import orm
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session, relationship

#engine = psycopg2.connect(dbname='postgres', user='postgres', password='976604745', host='localhost')

engine = create_engine('postgresql://postgres:976604745@localhost:5432/postgres')
SessionFactory = sessionmaker(bind=engine)
Session = scoped_session(SessionFactory)

#cursor = engine.cursor()

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    uid = Column(Integer, unique=True)
    username = Column(String, primary_key=True)
    password = Column(String)
    role = Column(Integer)


class City(Base):
    __tablename__ = 'cities'

    cid = Column(Integer, unique=True)
    name = Column(String, primary_key=True)


class AD(Base):
    __tablename__ = 'ads'

    adid = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(String)
    author = Column(String, ForeignKey(User.username))
    city = Column(String, ForeignKey(City.name))

    from_user = orm.relationship(User, foreign_keys=[author], backref='adinfo_from', lazy='joined')

    from_city = orm.relationship(City, foreign_keys=[city], backref='adinf_from', lazy='joined')
    #author = relationship('User', backref='adinfo')
    #city = relationship('City', backref='adinfo')



#Base.metadata.create_all(engine)

