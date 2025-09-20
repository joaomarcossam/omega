import discord
from discord.ext import commands
from ..core.settings import Env
from utils.font import Font
from ..modules.omegon import Omegon
from ..modules.hello import Hello

def create_bot():
    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix="?", intents=intents)

    # registrar cogs
    bot.add_cog(Omegon(bot))
    bot.add_cog(Hello(bot))

    return bot

def run():
    Env.load()
    bot = create_bot()
    print(Font("Omegon is starting...").blink.cyan)
    bot.run(Env.OMEGON_TOKEN)
