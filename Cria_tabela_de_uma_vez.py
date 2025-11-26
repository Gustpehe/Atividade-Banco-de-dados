from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
from Modelo_tabelas import Base

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
