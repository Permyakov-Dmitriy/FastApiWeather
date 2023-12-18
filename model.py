from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = "postgresql://postgres:1234@postgres/weather"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

Base = declarative_base()

class History(Base):
    __tablename__ = 'history'

    id = Column(Integer, primary_key=True, index=True)
    city = Column(String)
    weather = Column(String)
    temp = Column(Integer)
    wind = Column(Float)
    token = Column(String)


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String)


Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autoflush=False, bind=engine)
db = SessionLocal()
