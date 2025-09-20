from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pymysql
from pymysql.cursors import DictCursor

from discord_bot.core.settings import Env

# carrega variáveis
Env.load()

# ---------- PyMySQL (modo manual) ----------
def get_connection():
    return pymysql.connect(
        host=Env.DB_HOST,
        port=Env.DB_PORT,
        user=Env.DB_USER,
        password=Env.DB_PASS,
        database=Env.DB_NAME,
        cursorclass=DictCursor,
    )

# ---------- SQLAlchemy (modo ORM) ----------
DATABASE_URL = f"mysql+pymysql://{Env.DB_USER}:{Env.DB_PASS}@{Env.DB_HOST}:{Env.DB_PORT}/{Env.DB_NAME}"

engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
