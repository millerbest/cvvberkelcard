from .. import models
from pathlib import Path
import json
import xlsxwriter


def get_missing_players_raw() -> dict[str, list[str]]:
    """Get a summary of missing player cards by team, return as a dict"""
    result = {}
    teams = models.Team.objects.all().order_by("pk")
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
        {
            "bold": True,
            "font_color": "white",
            "bg_color": "#38761D",
            "align": "center",
            "valign": "vcenter",
            "border": 1,
        }
    )
    worksheet.set_column("A:A", 20)

    current_row = 1  # Start writing from the second row (Index 1)
    current_column = 0  # Start from the first column for each team

    MAX_ROW = 40

    for team_name, players in missing_players.items():

        # Write the Team Header Row
        worksheet.write(current_row, current_column, team_name, team_fmt)
        current_row += 1

        # Write each player on a new row under the team
        for player in players:
            worksheet.write(current_row, current_column, player, player_fmt)
            current_row += 1

        # Optional: Add an empty row between teams for visual breathing room
        current_row += 1
        if current_row >= MAX_ROW:
            current_row = 1  # Reset to the second row
            current_column += 2  # Move to the next set of columns for the next team
            worksheet.set_column(current_column - 1, current_column - 1, 2)
            worksheet.set_column(current_column, current_column, 20)
    # Setup Headers
    # TODO： combine cells and center the header text across the top of the page
    worksheet.merge_range(
        0, 0, 0, current_column, "C.V.V BERKEL VOETBALPLAATJESACTIE", header_fmt
    )

    workbook.close()


def write_missing_players_to_pdf(
    missing_players: dict[str, list[str]], output_path: Path
) -> None:
    raise NotImplementedError("PDF output not implemented yet")
