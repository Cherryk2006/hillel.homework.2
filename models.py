from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    login = Column(String(50), unique=True)
    password = Column(String(50))
    ipn = Column(Integer, unique=True)
    full_name = Column(String(150))
    contacts = Column(String(150))
    photo = Column(String(150))

    def __init__(self, login, password, ipn, full_name, contacts, photo):
        self.login = login
        self.password = password
        self.ipn = ipn
        self.full_name = full_name
        self.contacts = contacts
        self.photo = photo


class Item(Base):
    __tablename__ = 'item'
    id = Column(Integer, primary_key=True, autoincrement=True)
    photo = Column(String(150))
    name = Column(String(50), unique=True)
    description = Column(String(150))
    price_hour = Column(Integer)
    price_day = Column(Integer)
    price_month = Column(Integer)
    price_year = Column(Integer)
    owner_id = Column(Integer, ForeignKey('user.id'))

    def __init__(self, photo, name, description, price_hour, price_day, price_month, price_year, owner_id):
        self.photo = photo
        self.name = name
        self.description = description
        self.price_hour = price_hour
        self.price_day = price_day
        self.price_month = price_month
        self.price_year = price_year
        self.owner_id = owner_id

    def __repr__(self):
        return f'<Item {self.name}>, {self.id}, {self.owner_id}'