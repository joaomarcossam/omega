from discord.ext import commands
from ..core.settings import Env
from utils.font import Font
from ..modules.logchannel import LogChannel
from ..modules.omegon import Omegon
from ..modules.hello import Hello

def create_bot():
    intents = commands.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix="?", intents=intents)
    return bot

async def register_cogs(bot):
    await bot.add_cog(Omegon(bot))
    await bot.add_cog(Hello(bot))
    await bot.add_cog(LogChannel(bot))

def run():
    Env.load()
    bot = create_bot()
    print(Font("Omegon is starting...").blink.cyan)

    # usa asyncio.run para iniciar com setup assíncrono
    import asyncio

    async def runner():
        await register_cogs(bot)
        await bot.start(Env.OMEGON_TOKEN)

    asyncio.run(runner())
