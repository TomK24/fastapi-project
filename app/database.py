from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
from time import time
from .config import settings

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db(): #We call this function every time we get a API request that requires db access
    db = SessionLocal() #this object actually talks to the db.
    try:
        yield db
    finally:
        db.close()

#Connecting to database if not using SQLAlchemy
# while True:
#     try:
#         conn = psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='1234', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print('database connection was successful')
#         break
#     except Exception as error:
#         print('connection failed')
#         print("Error: ", error)
#         time.sleep(2)