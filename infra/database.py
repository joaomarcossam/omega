import os
import pymysql
from pymysql.cursors import DictCursor

def get_connection():
    return pymysql.connect(
        host=os.getenv("DB_HOST", "us.mysql.db.bot-hosting.net"),
        port=int(os.getenv("DB_PORT", 3306)),
        user=os.getenv("DB_USER", "u483539_IVFUQqVTUC"),
        password=os.getenv("DB_PASS", "RrYofY!kn^9TydvcxA!nN@tf"), #Todo: mudar para variavel de ambiente
        database=os.getenv("DB_NAME", "s483539_omega_db"),
        cursorclass=DictCursor,
    )