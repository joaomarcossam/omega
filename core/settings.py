import os
from dotenv import load_dotenv

load_dotenv()

class Env:
    @staticmethod
    def load():
        Env.OMEGON_TOKEN = os.getenv("OMEGON_TOKEN")
        Env.TESTE = os.getenv("TESTE")


def main():
    print(os.environ.get('TESTE'))
    print(os.environ.get('OMEGON_TOKEN'))


if __name__=="__main__":
    main()