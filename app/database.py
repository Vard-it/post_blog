from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import psycopg2
from psycopg2.extras import RealDictCursor
import time

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:rose100@localhost/PostBlog'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close_all()


while True:
    try:
        conn = psycopg2.connect(
            host='localhost',
            database='PostBlog',
            user='postgres',
            password='rose100',
            cursor_factory=RealDictCursor
        )
        cursor = conn.cursor()

        print("DB connection was successful ! ")
        break

    except Exception as error:
        time.sleep(2)
        print("Connecting to DB failed, error was -> ", error)

