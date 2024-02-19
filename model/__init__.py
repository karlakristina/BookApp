from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

#XAMP MySQL
#engine = create_engine("mysql+pymysql://root@localhost:3306/books")

engine = create_engine("mysql+pymysql://book:book123@mysql:3306/book") 

Session = sessionmaker(bind=engine)

Session = Session()

Base = declarative_base()