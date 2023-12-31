from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from decouple import config

DB_HOST = config('DB_HOST')
DB_NAME = config('DB_NAME')
DB_USER = config('DB_USER')
DB_PASSWORD = config('DB_PASSWORD')
DB_PORT = config('DB_PORT')

# Construct the DATABASE_URL
sqlalchemy_url = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(sqlalchemy_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


"""for reference"""

"""
import psycopg2
import time
from psycopg2.extras import RealDictCursor


host = config('HOST')
database = config('DATABASE')
user = config('USER')
password = config('PASSWORD')


while True:
    try:
        conn = psycopg2.connect(host="localhost", database="fastapi", user="postgres", password="mankindjnr", cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("DATABSE CONN IS A SUCCESS")
        break
    except Exception as error:
        print("DATABSE CONN IS A FAILURE", error)
        time.sleep(2)
"""