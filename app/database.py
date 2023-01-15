from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import time
import psycopg2
from psycopg2.extras import RealDictCursor
from .config import settings

# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
db_name = settings.database_name
db_port = settings.database_port
db_user = settings.database_username
db_password = settings.database_password
db_hostname = settings.database_hostname

SQLALCHEMY_DATABASE_URL = f'postgresql://{db_user}:{db_password}@{db_hostname}:{db_port}/{db_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit= False, autoflush= False, bind = engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()

# while True:
#     try:
#         conn = psycopg2.connect(host = 'localhost', database = "fastapi", 
#                                 user = 'postgres', password = "password", cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("connected to db")
#         break
#     except Exception as error: 
#         print("Connection failed")
#         print(error)
#         time.sleep(3)

