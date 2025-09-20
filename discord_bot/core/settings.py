import os
from dotenv import load_dotenv

load_dotenv()

class Env:
    @staticmethod
    def load():
        # Tokens
        Env.OMEGON_TOKEN = os.getenv("OMEGON_TOKEN")

        # Banco de dados
        Env.DB_USER = os.getenv("DB_USER")
        Env.DB_PASS = os.getenv("DB_PASS")
        Env.DB_HOST = os.getenv("DB_HOST")
        Env.DB_PORT = int(os.getenv("DB_PORT", 3306))
        Env.DB_NAME = os.getenv("DB_NAME")


def main():
    print(os.environ.get('TESTE'))
    print(os.environ.get('OMEGON_TOKEN'))


if __name__=="__main__":
    main()