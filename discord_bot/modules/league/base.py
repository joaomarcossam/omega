from discord.ext import commands
from services.riot.riot_service import RiotService
from logging import getLogger
import discord

TIER_COLORS = {
    "IRON": discord.Color.dark_gray(),
    "BRONZE": discord.Color.dark_orange(),
    "SILVER": discord.Color.light_gray(),
    "GOLD": discord.Color.gold(),
    "PLATINUM": discord.Color.teal(),
    "EMERALD": discord.Color.green(),
    "DIAMOND": discord.Color.blue(),
    "MASTER": discord.Color.purple(),
    "GRANDMASTER": discord.Color.red(),
    "CHALLENGER": discord.Color.magenta(),
}

class LeagueBase(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.service = RiotService()
        self.logger = getLogger("discord_logs")

    def split_riot_id(self, riot_id: str):
        if "#" not in riot_id:
            return None, None
        return riot_id.split("#", 1)

    def make_embed(self, title: str, description: str, color=discord.Color.default()):
        return discord.Embed(title=title, description=description, color=color)
