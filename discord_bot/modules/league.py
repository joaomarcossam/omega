from logging import getLogger
from discord.ext import commands
from services.riot_service import RiotService

logger = getLogger("discord_logs")

QUEUE_MAP = {
    "RANKED_SOLO_5x5": "Solo/Duo",
    "RANKED_FLEX_SR": "Flex",
}

class League(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.service = RiotService()

    @commands.command(name="elo")
    async def elo(self, ctx, riot_id: str, platform: str = "br1"):
        msg = ""
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

            msg = f"🔹 Invocador: **{data['name']}** (Level {data['level']})\n"
            ranks = data.get("ranks") or []

            if not ranks:
                logger.warning("No ranks found for %s#%s", game_name, tag_line)
                msg += "Sem dados ranqueados.\n"
            else:
                for entry in ranks:
                    queue = QUEUE_MAP.get(entry.get("queueType"), entry.get("queueType"))
                    tier = entry.get("tier", "UNRANKED")
                    rank = entry.get("rank", "")
                    lp = entry.get("leaguePoints", 0)
                    wins = entry.get("wins", 0)
                    losses = entry.get("losses", 0)

                    if tier == "UNRANKED":
                        msg += f"{queue}: UNRANKED\n"
                    else:
                        msg += f"{queue}: {tier} {rank} - {lp} PDL ({wins}W/{losses}L)\n"

            logger.info("Elo result sent for %s", ctx.author)

        except Exception as e:
            logger.exception(f"Erro ao buscar elo de {riot_id} ({platform}): {e}")
            await ctx.send("❌ Ocorreu um erro ao buscar os dados. Tente novamente mais tarde.")
            return

        await ctx.send(msg)
