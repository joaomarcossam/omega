import os
from dotenv import load_dotenv

load_dotenv()

class Env:
    @staticmethod
    def load():
        # Tokens
        Env.OMEGON_TOKEN = os.getenv("OMEGON_TOKEN")

        # Banco de dados
        Env.DB_USER = os.getenv("DB_USER", "u483539_IVFUQqVTUC")
        Env.DB_PASS = os.getenv("DB_PASS", "RrYofY!kn^9TydvcxA!nN@tf")  # cuidado: senha em claro
        Env.DB_HOST = os.getenv("DB_HOST", "us.mysql.db.bot-hosting.net")
        Env.DB_PORT = int(os.getenv("DB_PORT", 3306))
        Env.DB_NAME = os.getenv("DB_NAME", "s483539_omega_db")
        Env.RIOT_API_KEY = os.getenv("RIOT_API_KEY")
        Env.RIOT_API_KEY = os.getenv("RIOT_API_KEY", 'br1')


def main():
    print(os.environ.get('TESTE'))
    print(os.environ.get('OMEGON_TOKEN'))


if __name__=="__main__":
    main()