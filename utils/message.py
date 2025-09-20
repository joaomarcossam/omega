from .font import Font

class Message:
    def ok(x = None):
        if x:
            cursor = f"\033[{x}G"
        else :
            cursor = ""

        print(f"{cursor}{(Font('✓ OK').bold.blue.s)}")

    def fail(x = 0):
        if x:
            cursor = f"\033[{x}G"
        else :
            cursor = ""

        print(f"{cursor}{(Font('✗ FAIL').red.s)}")
