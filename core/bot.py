import discord
from discord.ext import commands
from core.settings import Env
from modules import Omegon
from utils.font import Font


def create_bot():
    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix="?", intents=intents)

    # Carregar cogs
    bot.add_cog(Omegon(bot))
    return bot

def run():
    Env.load()
    bot = create_bot()
    print(Font("Omegon is starting...").blink.cyan)
    bot.run(Env.OMEGON_TOKEN)
