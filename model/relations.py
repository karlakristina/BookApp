
from sqlalchemy.orm import relationship
from users import User
from books import Book
from category import Category
from cart import Cart
from library import Library


from __init__ import Base
from __init__  import engine


User.books = relationship('Book', back_populates='users')
User.category = relationship("Category", back_populates="users")
User.cart = relationship('Cart', back_populates='users')
Category.books = relationship('Book', back_populates='categories')
Category.cart = relationship('Cart', back_populates='categories')
Book.cart = relationship('Cart', back_populates='books')

Base.metadata.bind = engine
Base.metadata.create_all(bind=engine)