from __init__ import Base
from sqlalchemy import *


class User (Base):
    __tablename__ = "users"
    ID_user = Column(Integer, primary_key = True)
    firstName = Column(String(50))
    lastName =Column(String(50))
    email = Column(String(50))
    password=Column(String(50))