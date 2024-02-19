from __init__ import Base

from sqlalchemy import *


class Cart (Base):
    __tablename__ = "cart"
    ID_cart = Column(Integer, primary_key = True)
    user_id = Column(Integer,ForeignKey("users.ID_user", ondelete="CASCADE"))
    category_id = Column(Integer, ForeignKey("categories.ID_category",ondelete="CASCADE"))
    book_id = Column(Integer, ForeignKey("books.ID_book",ondelete="CASCADE"))