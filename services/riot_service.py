from infra.riot_api import RiotAPI

class RiotService:
    def __init__(self):
        self.api = RiotAPI()

    async def get_player_info(self, summoner_name: str):
        summoner = await self.api.get_summoner_by_name(summoner_name)
        if not summoner:
            return None

        ranks = await self.api.get_rank_by_puuid(summoner["puuid"])
        return {
            "name": summoner["name"],
            "level": summoner["summonerLevel"],
            "ranks": ranks,
        }
