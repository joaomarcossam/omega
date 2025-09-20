from discordia.omegon import Omegon
from environment import Env
from utils.font import Font

def main():
    Env.load()
    print(Font("Booting Omegon...").cyan)
    omegon = Omegon()
    omegon.run()

if __name__ == "__main__":
    main()
