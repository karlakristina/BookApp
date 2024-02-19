from __init__ import Base

from sqlalchemy import *


class Book (Base):
    __tablename__ = "books"
    ID_book = Column(Integer, primary_key = True)
    user_id = Column(Integer,ForeignKey("users.ID_user", ondelete="CASCADE"))
    category_id = Column(Integer,ForeignKey("categories.ID_category", ondelete="CASCADE"))
    name = Column(String(50))
    author=Column(String(50))
    year = Column(Integer)
    price=Column(Float)
    description =Column(String(500))
    image = Column(String(100), nullable=False, unique=True)