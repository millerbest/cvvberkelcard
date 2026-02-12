import json
from ..models import Team, PlayerCard


def import_players(file_path: str):
    with open(file_path, "r") as f:
        data = json.load(f)
        for player_data in data:
            player_name = player_data["name"]
            team_name = player_data["team"]
            team = Team.objects.filter(name=team_name).first()
            player, created = PlayerCard.objects.get_or_create(
                name=player_name, team=team
            )
            if created:
                print(f"Created player: {player_name}")
            else:
                print(f"Player already exists: {player_name}")
