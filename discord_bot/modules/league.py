from logging import getLogger
import discord
from discord.ext import commands
from services.riot_service import RiotService

logger = getLogger("discord_logs")

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


class League(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.service = RiotService()

    @commands.command(name="elo")
    async def elo(self, ctx, riot_id: str, platform: str = "br1"):
        try:
            logger.info("Elo command called by %s", ctx.author)

            if "#" not in riot_id:
                await ctx.send("❌ Formato inválido. Use: `?elo Nome#TAG [plataforma]`")
                return

            game_name, tag_line = riot_id.split("#", 1)
            data = await self.service.get_player_info(game_name, tag_line, platform)

            if not data:
                logger.warning("Player not found for %s#%s", game_name, tag_line)
                await ctx.send("❌ Jogador não encontrado!")
                return

            ranks = data.get("ranks") or []
            tier_main = ranks[0].get("tier", "UNRANKED") if ranks else "UNRANKED"

            # --- Embed bonito ---
            embed = discord.Embed(
                title=f"🔹 Invocador: {data['name']}",
                description=f"Nível **{data['level']}**",
                color=TIER_COLORS.get(tier_main, discord.Color.default())
            )

            # Ícone de perfil do invocador
            if data.get("profileIconId"):
                embed.set_thumbnail(
                    url=f"http://ddragon.leagueoflegends.com/cdn/14.17.1/img/profileicon/{data['profileIconId']}.png"
                )

            if not ranks:
                embed.add_field(name="Elo", value="❌ Unranked", inline=False)
            else:
                for entry in ranks:
                    queue = entry.get("queueType", "QUEUE")
                    tier = entry.get("tier", "UNRANKED")
                    rank = entry.get("rank", "")
                    lp = entry.get("leaguePoints", 0)
                    wins = entry.get("wins", 0)
                    losses = entry.get("losses", 0)

                    fila = "🗡️ Solo/Duo" if queue == "RANKED_SOLO_5x5" else "🛡️ Flex"
                    value = f"**{tier} {rank}** - {lp} PDL\n📊 {wins}W / {losses}L"
                    embed.add_field(name=fila, value=value, inline=True)

            embed.set_footer(text="Dados fornecidos pela Riot API")

            await ctx.send(embed=embed)
            logger.info("Elo result sent for %s", ctx.author)

        except Exception as e:
            logger.exception(f"Erro ao buscar elo de {riot_id} e {platform}. Erro: {e}")
            await ctx.send("⚠️ Ocorreu um erro ao buscar os dados.")
