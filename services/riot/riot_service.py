import aiohttp

from .riot_api_service import RiotAPIService
from logging import getLogger

logger = getLogger("discord_logs")

class RiotService(RiotAPIService):
    """Camada de orquestração: combina múltiplas chamadas + cache."""
    def __init__(self):
        super().__init__()
        self._champions = {}
        self._champions_loaded = False

    async def load_champions(self, version="14.17.1", lang="pt_BR"):
        """Carrega e cacheia os campeões do Data Dragon."""
        url = f"http://ddragon.leagueoflegends.com/cdn/{version}/data/{lang}/champion.json"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                data = await resp.json()
                for champ in data["data"].values():
                    self._champions[int(champ["key"])] = {
                        "id": champ["id"],
                        "name": champ["name"],
                        "icon": f"http://ddragon.leagueoflegends.com/cdn/{version}/img/champion/{champ['image']['full']}"
                    }
        self._champions_loaded = True
        logger.info("Champion data carregado com sucesso (%s campeões)", len(self._champions))

    def get_champion(self, champion_id: int):
        """Retorna info do campeão pelo ID."""
        if not self._champions_loaded:
            raise RuntimeError("Champion data ainda não carregado. Chame load_champions() primeiro.")
        return self._champions.get(champion_id, {"name": f"Desconhecido ({champion_id})", "icon": None})

    async def get_player_info(self, game_name: str, tag_line: str, platform: str = "br1"):
        """
        Une múltiplas chamadas (account + summoner + ranks)
        para entregar dados básicos (usado no !elo).
        """
        try:
            account = await self.get_account_by_riot_id(game_name, tag_line)
            if not account or "puuid" not in account:
                return None

            puuid = account["puuid"]
            summoner = await self.get_summoner_by_puuid(puuid, platform)
            if not isinstance(summoner, dict):
                return None

            ranks = await self.get_league_entries_by_puuid(puuid, platform) or []

        except Exception as e:
            logger.error(f"Erro ao buscar dados do jogador {game_name}#{tag_line}: {e}")
            return None

        return {
            "name": account.get("gameName") or summoner.get("name"),
            "level": summoner.get("summonerLevel"),
            "profileIconId": summoner.get("profileIconId"),
            "summonerId": summoner.get("id"),
            "puuid": puuid,
            "ranks": ranks,
        }

    async def get_player_profile(self, game_name: str, tag_line: str, platform: str = "br1"):
        base = await self.get_player_info(game_name, tag_line, platform)
        if not base:
            return None

        mastery = await self.get_champion_mastery_by_puuid(base["puuid"], platform) or []
        top_champions = mastery[:3]  # pega top 3
        total_points = sum(m["championPoints"] for m in mastery)

        champs_info = []
        if top_champions:
            if not self._champions_loaded:
                await self.load_champions()

            for champ in top_champions:
                champ_info = self.get_champion(champ["championId"])
                champs_info.append({
                    "id": champ["championId"],
                    "points": champ["championPoints"],
                    "name": champ_info["name"],
                    "icon": champ_info["icon"],
                })

        return {
            **base,
            "top_champions": champs_info,
            "total_mastery_points": total_points,
        }

