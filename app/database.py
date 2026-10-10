""" This file is responsible for setting up the database connection and creating a cursor object to interact with the database.
Basically connecting to the database and creating a cursor object to interact with the database. """

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import psycopg
import time
from config import settings
from sqlalchemy import URL, create_engine


database_url = URL.create(
    drivername="postgresql+psycopg",
    username=settings.database_username,
    password=settings.database_password,
    host=settings.database_hostname,
    port=settings.database_port,
    database=settings.database_name,
)

engine = create_engine(database_url)


SessionLocal = sessionmaker(expire_on_commit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal() # Responsible for creating a session to interact with the database.
    try:
        yield db
    finally:
        db.close()


# password = "post@express24"


# while True:
#     try:
#         conn = psycopg.connect(f"dbname=fastapi user=postgres password={password} host=localhost port=5432",  cursor_factory= RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connection was successful!")
#         break
#     except Exception as error:
#         print("Connecting to the database failed")
#         print("Error: ", error)
#         time.sleep(2)
