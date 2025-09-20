from modules.omegon import Omegon
from utils.font import Font

def main():
    print(Font("Booting Omegon...").cyan)
    omegon = Omegon()
    omegon.run()

if __name__ == "__main__":
    main()
