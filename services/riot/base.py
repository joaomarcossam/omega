from logging import getLogger
from infra.riot_api import RiotAPI

class RiotBaseService:
    def __init__(self):
        self.api = RiotAPI()
        self.logger = getLogger("discord_logs")
