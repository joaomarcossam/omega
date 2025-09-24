from logging import getLogger
from infra.riot_api import RiotAPI

logger = getLogger("discord_logs")


class RiotService:
    def __init__(self):
        self.api = RiotAPI()

    async def get_player_info(self, game_name: str, tag_line: str, platform: str = "br1"):
        try:
            logger.info(f"Getting player info for {game_name}#{tag_line}")

            # 1) RiotID → PUUID (regional)
            account = await self.api.get_account_by_riot_id(game_name, tag_line)
            if not isinstance(account, dict):
                logger.error(f"Account payload inválido: {account}")
                return None

            puuid = account.get("puuid")
            if not puuid:
                logger.error(f"PUUID não encontrado em account: {account}")
                return None

            # 2) PUUID → Summoner (opcional, só pra pegar level/icon)
            summoner = await self.api.get_summoner_by_puuid(puuid, platform)
            if not isinstance(summoner, dict):
                logger.error(f"Summoner payload inválido: {summoner}")
                return None

            # 3) PUUID → Ranked entries
            entries = await self.api.get_league_entries_by_puuid(puuid, platform)
            if entries is None:
                logger.warning(f"Sem ranked data para {puuid}")
                entries = []

            return {
                "name": account.get("gameName") or summoner.get("name"),
                "level": summoner.get("summonerLevel"),
                "ranks": entries,
            }

        except Exception as e:
            logger.exception(f"Erro ao buscar player {game_name}#{tag_line}: {e}")
            return None
