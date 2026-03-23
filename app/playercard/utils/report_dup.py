from .. import models
from pathlib import Path
import json
import xlsxwriter


def get_dup_players_raw() -> dict[str, list[models.PlayerCard]]:
    """Get a summary of duplicate player cards by team, return as a dict"""
    result = {}
    teams = models.Team.objects.all().order_by("pk")
    for team in teams:
        result[team.name] = []
        duplicate_players = models.PlayerCard.objects.filter(
            team=team, is_collected=True, duplicate_count__gt=0
        )
        for player in duplicate_players:
            result[team.name].append(player)
    return result


def write_dup_players_to_file(output_path: Path) -> None:
    """Write the duplicate players summary to a file in the specified format (json, xlsx, pdf)"""
    duplicate_players = get_dup_players_raw()
    extension = output_path.suffix.lower()
    mapping = {
        ".json": write_dup_players_to_json,
        ".xlsx": write_dup_players_to_xlsx,
        ".pdf": write_dup_players_to_pdf,
    }
    if extension in mapping:
        mapping[extension](duplicate_players, output_path)
    else:
        raise ValueError(f"Unsupported file format: {extension}")


def write_dup_players_to_json(
    duplicate_players: dict[str, list[models.PlayerCard]], output_path: Path
) -> None:
    with open(output_path, "w") as f:
        json.dump(
            {
                team: [
                    f"{player.name} - {player.duplicate_count}" for player in players
                ]
                for team, players in duplicate_players.items()
            },
            f,
            indent=4,
        )


def write_dup_players_to_xlsx(
    duplicated_players: dict[str, list[models.PlayerCard]], output_path: Path
) -> None:

    workbook = xlsxwriter.Workbook(output_path)
    worksheet = workbook.add_worksheet("Duplicated Players")

    # Define Formats
    header_fmt = workbook.add_format(
        {"bold": True, "border": 1, "bg_color": "#C5D9F1", "align": "center"}
    )
    cell_fmt_1 = workbook.add_format(
        {
            "border": 1,
            "align": "center",
            "valign": "vcenter",
            "bg_color": "#FDE9D9",
        }
    )
    cell_fmt_2 = workbook.add_format(
        {
            "border": 1,
            "align": "center",
            "valign": "vcenter",
            "bg_color": "#FDFDFD",
        }
    )
    mark_fmt1 = workbook.add_format(
        {
            "font_name": "Consolas",
            "font_size": 12,
            "border": 1,
            "align": "left",  # Left align looks better for tracking
            "valign": "vcenter",
            "bg_color": "#FDE9D9",
        }
    )
    mark_fmt2 = workbook.add_format(
        {
            "font_name": "Consolas",
            "font_size": 12,
            "border": 1,
            "align": "left",  # Left align looks better for tracking
            "valign": "vcenter",
            "bg_color": "#FDFDFD",
        }
    )
    # Set column widths for readability
    worksheet.set_column("A:A", 20)
    worksheet.set_column("B:B", 25)
    worksheet.set_column("C:C", 30)

    # Headers
    worksheet.write("A1", "Team", header_fmt)
    worksheet.write("B1", "Player Name", header_fmt)
    worksheet.write("C1", "Available Cards", header_fmt)

    current_row = 1  # Start after header

    for team_count, (team_name, players) in enumerate(duplicated_players.items()):
        start_row = current_row

        for player in players:
            # Generate circles based on duplicate_counts
            boxes = "☐ " * player.duplicate_count

            # Write Player Name and Circles
            cell_fmt = cell_fmt_1 if team_count % 2 == 0 else cell_fmt_2
            mark_fmt = mark_fmt1 if team_count % 2 == 0 else mark_fmt2

            worksheet.write(current_row, 1, player.name, cell_fmt)
            worksheet.write(current_row, 2, boxes, cell_fmt)
            worksheet.write(current_row, 2, boxes, mark_fmt)
            current_row += 1

        end_row = current_row - 1

        # Merge Team Name column
        if start_row == end_row:
            # If only one player, no need to merge
            worksheet.write(start_row, 0, team_name, cell_fmt)
        else:
            worksheet.merge_range(start_row, 0, end_row, 0, team_name, cell_fmt)

    workbook.close()


def write_dup_players_to_pdf(
    duplicate_players: dict[str, list[models.PlayerCard]], output_path: Path
) -> None:
    raise NotImplementedError("PDF output not implemented yet")
