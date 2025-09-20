from os import environ
import inspect
from dotenv import load_dotenv

from utils.font import Font

load_dotenv()

def main():
    print(environ.get('TESTE'))
    print(environ.get('OMEGON_TOKEN'))


if __name__=="__main__":
    main()