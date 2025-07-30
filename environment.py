import os
import inspect
from dotenv import dotenv_values

from utils.font import Font
from utils.message import Message

class EnvHandler:
    def __init__(self, env_dict: dict):
        for key, value in env_dict.items():
            self.__setattr__(key, value)
    
    @staticmethod
    def load():
        try:
            frame = inspect.stack()[1]
            subpath = os.path.relpath(frame.filename).split(os.sep)
            folder = "/".join(subpath[:-1])
            current_file = subpath[-1]
        
            print(Font(f"- Loading envs: {Font(current_file).underline}").green, end="")
            Message.ok(x=30)
            envs = dotenv_values(f"{folder}/.env")
            
            return EnvHandler(envs)
        
        except Exception:
            Message.fail(rjust=25)
            raise
        