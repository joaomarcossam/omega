import os
import inspect
from dotenv import dotenv_values

from utils.font import Font

class EnvMeta(type):
    def __getattr__(cls, name: str):
        if name in cls.keyvals:
            return cls.keyvals[name]
        if name in os.environ:
            return os.environ[name]
        raise AttributeError(f"Variável de ambiente '{name}' não definida")

        
class Env(metaclass=EnvMeta):
    keyvals = {}
    
    @staticmethod
    def load(module: str = None):
        if module:
            path = Env._path_from_module(module)
        else:
            path = Env._path_from_current_module()
        
        Env.keyvals |= dotenv_values(dotenv_path=path)

    @staticmethod
    def _path_from_module(module):
        if module not in os.listdir("."):
            raise ModuleNotFoundError("Diretório não encontrado")
        
        if not os.path.isdir(module): 
            raise NotADirectoryError("O caminho não é um diretório")
        
        return f"{module}/.env"
    @staticmethod
    def _path_from_current_module():
        frame = inspect.stack()[1]
        subpath = os.path.relpath(frame.filename).split(os.sep)
        path = "/".join(subpath[:-1])
        
        return f"{path}/.env".strip("/")

    @staticmethod    
    def list():
        for key, value in Env.keyvals.items():
            print(f"{Font(key).bold}: {Font(value).blue.bold}")
    

if __name__ == "__main__":
    Env.load()
    