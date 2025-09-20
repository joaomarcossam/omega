from discord.ext import commands
import os
from modules import omegon, hello

class Bot(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(command_prefix="?", intents=kwargs.get("intents"))
        self.load_extensions()

    def load_extensions(self):

        self.add_cog(omegon.Omegon(self))
        self.add_cog(hello.Hello(self))
