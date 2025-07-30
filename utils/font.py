class Font:
    def __init__(self, content: str):
        self.content = content

    @property
    def blue(self):
        self.content = f'\033[34m{self.content}'
        return self

    @property
    def green(self):
        self.content = f"\033[32m{self.content}"
        return self

    @property
    def red(self):
        self.content = f"\033[31m{self.content}"
        return self
    
    @property
    def yellow(self):
        self.content = f"\033[33m{self.content}"
        return self
    
    @property
    def cyan(self):
        self.content = f"\033[36m{self.content}"
        return self
    
    @property
    def magenta(self):
        self.content = f"\033[35m{self.content}"
        return self
    
    @property
    def white(self):
        self.content = f"\033[37m{self.content}"
        return self
    
    @property
    def black(self):
        self.content = f"\033[30m{self.content}"
        return self
    
    @property
    def bold(self):
        self.content = f"\033[1m{self.content}"
        return self
    
    @property
    def underline(self):
        self.content = f"\033[4m{self.content}"
        return self

    @property
    def blink(self):
        self.content = f"\033[5m{self.content}"
        return self
    
    @property
    def reverse(self):
        self.content = f"\033[7m{self.content}"
        return self
    
    @property
    def hidden(self):
        self.content = f"\033[8m{self.content}"
        return self
    
    @property
    def strikethrough(self):
        self.content = f"\033[9m{self.content}"
        return self
    
    @property
    def double_underline(self):
        self.content = f"\033[21m{self.content}"
        return self
    
    @property
    def overline(self):
        self.content = f"\033[53m{self.content}"
        return self
    
    @property
    def italic(self):
        self.content = f"\033[3m{self.content}"
        return self

    @property
    def s(self):
        return f"{self.content}\033[0m"

    def __str__(self):
        return f"{self.content}\033[0m"
    
def main():
    print(Font("Hello").yellow)
    print(Font("Hello").yellow.bold.underline)

if __name__ == "__main__":
    main()