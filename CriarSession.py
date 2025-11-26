from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os


def roda_essa_bomba(URL):
    load_dotenv()

    DATABASE_URL = os.getenv(URL)

    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    return Session
