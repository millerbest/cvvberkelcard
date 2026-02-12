import json
from ..models import Team


def import_team(file_path: str):
    with open(file_path, "r") as f:
        data = json.load(f)
        for player_data in data:
            team_name = player_data["team"]
            team, created = Team.objects.get_or_create(name=team_name)
            if created:
                print(f"Created team: {team_name}")
            else:
                print(f"Team already exists: {team_name}")
