import urllib.parse

def league_of_graphs_url(riot_id: str, region: str = "br"):
    game_name, tag_line = riot_id.split("#", 1)
    riot_id_dash = f"{game_name}-{tag_line}"
    encoded = urllib.parse.quote(riot_id_dash)
    return f"https://www.leagueofgraphs.com/pt/summoner/{region}/{encoded}"
