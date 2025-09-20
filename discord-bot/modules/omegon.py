import discord
from discord.ext import commands
from utils.font import Font
from utils.module import Module

class Omegon(commands.Cog, Module):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()

    # Evento quando o bot fica online
    @commands.Cog.listener()
    async def on_ready(self):
        print(Font("♪ Omegon bot is ready!").cyan.double_underline.bold)

    # Evento ao receber mensagem
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        await self.bot.process_commands(message)

    # Comando de teste
    @commands.command(name="hello")
    async def hello(self, ctx): 
        await ctx.send("Hello! 🤔")

    @commands.command(name="card")
    async def hello(self, ctx, title: str = "", *, description: str = ""):
        embed = discord.Embed(
            title="Hello! 👋",
            description="Hello! 👋",
            color=discord.Color.green()
        )
        
        await ctx.send("Hello! 👋")

    # Comando para parar o bot
    @commands.command(name="stop")
    async def stop(self, ctx):
        await ctx.send("Bot is stopping...")
        print(f"{Font('Stopping Program...').black.bold}")
        Module.stop_all_modules()
