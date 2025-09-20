import os
import pymysql
from pymysql.cursors import DictCursor
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Variáveis de ambiente
DB_USER = os.getenv("DB_USER", "u483539_IVFUQqVTUC")
DB_PASS = os.getenv("DB_PASS", "RrYofY!kn^9TydvcxA!nN@tf")  # TODO: mudar para variável de ambiente segura
DB_HOST = os.getenv("DB_HOST", "us.mysql.db.bot-hosting.net")
DB_PORT = int(os.getenv("DB_PORT", 3306))
DB_NAME = os.getenv("DB_NAME", "s483539_omega_db")

# ---------- PyMySQL (modo manual) ----------
def get_connection():
    """
    Retorna uma conexão direta usando PyMySQL.
    Útil para consultas rápidas fora do ORM.
    """
    return pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME,
        cursorclass=DictCursor,
    )

# ---------- SQLAlchemy (modo ORM) ----------
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Engine
engine = create_engine(DATABASE_URL, echo=False, future=True)

# Session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para models
Base = declarative_base()
