from __init__ import Base

from sqlalchemy import *


class Category (Base):
    __tablename__ = "categories"
    ID_category = Column(Integer, primary_key = True)
    user_id = Column(Integer,ForeignKey("users.ID_user", ondelete="CASCADE"))
    name = Column(String(50))
    description =Column(String(200))
   