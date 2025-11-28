from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor  #used to show column names
import time
from .config import settings


SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()    #creates a new session
    try:
        yield db
    finally:
        db.close()


# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='ayush1106', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()   #cursor is used to help write sql queries
#         print("Database was connected successfully!")
#         break     #the loop will be breaked if database is connected
#     except Exception as error:
#         print("Connection to database failed")
#         print("Error: ", error)      #the loop will continue to try and connect the database(best practice when internet issue or when db is setting up)
#         time.sleep(3)      #will show error every 3secs, this is helpful because then the rest of the code won't run unnecessarily until the db is connected 

