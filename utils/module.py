from .font import Font
from .message import Message

class Module:
    module_stack = []
    def __init__(self):
        Module.add_module(self)

    def __str__(self):
        return self.__class__.__name__

    @property
    def name(self):
        return self.__class__.__name__

    @classmethod
    def add_module(cls, module):
        Module.module_stack.append(module)
    
    @classmethod
    def get_modules(cls):
        return cls.module_stack

    @classmethod
    def stop_all_modules(cls):
        while cls.module_stack:
            module = cls.module_stack.pop()
            module.stop()
        
        print(Font(" ✓ All modules stopped.").bold.green)

    def start(self):
        class_name = self.__class__.__name__
        print(Font(f"→ Starting module: {Font(class_name).underline}").cyan, end="")
        Message.ok(x=30)
        return self

    def stop(self):
        class_name = self.__class__.__name__
        print(Font(f"• Stopping module: {Font(class_name).underline}").yellow, end="")
        Message.ok(x=30)
        del self

