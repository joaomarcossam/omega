import discord
from discord.ext import commands
from utils.font import Font
from utils.module import Module

class Omegon(commands.Cog, Module):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()

    # (Opcional) Apenas manter o on_ready se quiser um "log" específico
    @commands.Cog.listener()
    async def on_ready(self):
        print(Font("♪ Omegon module loaded!").cyan.double_underline.bold)

    # Comando para parar o bot
    @commands.command(name="stop")
    async def stop(self, ctx):
        await ctx.send("Bot is stopping...")
        print(f"{Font('Stopping Program...').black.bold}")
        Module.stop_all_modules()
