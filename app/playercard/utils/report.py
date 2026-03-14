from .. import models
from pathlib import Path
import json
import xlsxwriter


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

    workbook = xlsxwriter.Workbook(output_path)
    worksheet = workbook.add_worksheet("Players")

    # Page Setup for A4 Printing
    worksheet.set_paper(9)  # 9 is the code for A4
    worksheet.set_margins(left=0.5, right=0.5, top=0.7, bottom=0.7)
    worksheet.set_column("A:C", 25)  # Set column widths

    # Define Formats
    team_fmt = workbook.add_format({"bold": True, "bg_color": "#D9EAD3", "border": 1})
    player_fmt = workbook.add_format(
        {"border": 1}
    )  # Indent makes it look like a sub-item
    header_fmt = workbook.add_format(
        {"bold": True, "font_color": "white", "bg_color": "#38761D"}
    )
    max_rows_per_page = 40  # Adjust this based on your font size/A4 height

    current_total_row = 0

    for team_name, players in missing_players.items():
        # Check if we need to wrap to the next column BEFORE starting a new team
        # We add +1 for the team header and len(players) for the roster
        if (current_total_row % max_rows_per_page) + len(
            players
        ) + 1 > max_rows_per_page:
            # Move to the start of the next column block
            current_total_row = (
                (current_total_row // max_rows_per_page) + 1
            ) * max_rows_per_page

        # Calculate current column (0, 1, or 2) and local row (0-39)
        col = (current_total_row // max_rows_per_page) % 3
        row = current_total_row % max_rows_per_page

        # Write Team Header
        worksheet.write(row, col, team_name, team_fmt)
        current_total_row += 1

        # Write Players
        for player in players:
            row = current_total_row % max_rows_per_page
            # Note: If a team is very long, it might split across columns here
            worksheet.write(row, col, player, player_fmt)
            current_total_row += 1

        # Add a spacer row between teams
        current_total_row += 1
    workbook.close()


def write_missing_players_to_pdf(
    missing_players: dict[str, list[str]], output_path: Path
) -> None:
    raise NotImplementedError("PDF output not implemented yet")
