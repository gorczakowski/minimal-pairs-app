from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
engine = create_engine('sqlite:///app_db.db', echo=False)

# class Session(Base):
#     __tablename__ = 'session'
#     id = Column(Integer, primary_key=True)
#     score = Column(Float)

class Pair(Base):
    __tablename__ = 'pair'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    tracks = relationship('Track', backref='pair')

class Track(Base):
    __tablename__ = 'track'
    id = Column(Integer, primary_key=True)
    pair_id = Column(Integer, ForeignKey('pair.id'))
    name = Column(String, unique=True)
    path = Column(String)

Base.metadata.create_all(engine)
