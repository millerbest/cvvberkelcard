from .. import models
from pathlib import Path
import json


def get_missing_players_raw() -> dict[str, list[str]]:
    """Get a summary of missing player cards by team, return as a dict"""
    result = {}
    teams = models.Team.objects.all().distinct()
    for team in teams:
        result[team.name] = []
        missing_players = models.PlayerCard.objects.filter(
            team=team, is_collected=False
        )
        for player in missing_players:
            result[team.name].append(player.name)
    return result


def write_missing_players_to_file(output_path: Path) -> None:
    """Write the missing players summary to a file in the specified format (json, xlsx, pdf)"""
    missing_players = get_missing_players_raw()
    extension = output_path.suffix.lower()
    mapping = {
        ".json": write_missing_players_to_json,
        ".xlsx": write_missing_players_to_xlsx,
        ".pdf": write_missing_players_to_pdf,
    }
    if extension in mapping:
        mapping[extension](missing_players, output_path)
    else:
        raise ValueError(f"Unsupported file format: {extension}")


def write_missing_players_to_json(
    missing_players: dict[str, list[str]], output_path: Path
) -> None:
    with open(output_path, "w") as f:
        json.dump(missing_players, f, indent=4)


def write_missing_players_to_xlsx(
    missing_players: dict[str, list[str]], output_path: Path
) -> None:
    raise NotImplementedError("Excel output not implemented yet")


def write_missing_players_to_pdf(
    missing_players: dict[str, list[str]], output_path: Path
) -> None:
    raise NotImplementedError("PDF output not implemented yet")
