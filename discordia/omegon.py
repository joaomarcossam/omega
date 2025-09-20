# discordia/omegon.py
import discord
from discord.ext import commands

from environment import Env
from utils.font import Font
from utils.module import Module

Env.load()

class Omegon(Module):
    def __init__(self):
        super().__init__()
        intents = discord.Intents.default()
        intents.message_content = True
        self.bot = commands.Bot(command_prefix='?', intents=intents)
        self.setup_events()
        self.setup_commands()

    def setup_events(self):
        @self.bot.event
        async def on_ready():
            print(Font("♪ Omegon bot is ready!").cyan.double_underline.bold)

        @self.bot.event
        async def on_message(message):
            if message.author == self.bot.user:
                return
            await self.bot.process_commands(message)

    def setup_commands(self):
        @self.bot.command(name='hello')
        async def hello(ctx):
            await ctx.send('Hello! 🤔')

        @self.bot.command(name='stop')
        async def stop(ctx):
            await ctx.send("Bot is stopping...")
            # Corrigido: aspas dentro do f-string
            print(f"{Font('\\nStoping Program...').black.bold}")
            Module.stop_all_modules()

    def run(self):
        print(Font("Omegon is starting...").blink.cyan)
        self.bot.run(Env.OMEGON_TOKEN)
