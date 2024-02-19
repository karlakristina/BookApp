from __init__ import Base
from sqlalchemy import *


class Library (Base):
    __tablename__ = "library"
    ID_library = Column(Integer, primary_key = True)
    name = Column(String(50))
    address =Column(String(50))
    phone_number = Column(Integer)