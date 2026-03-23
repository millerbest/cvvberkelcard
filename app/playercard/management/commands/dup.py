"""Get a summary in for missing player cards"""

from pathlib import Path
from datetime import datetime
from django.core.management.base import BaseCommand
from playercard.utils.report_dup import write_dup_players_to_file


def get_file_name(output_format: str) -> str:
    current_dt = datetime.now().strftime("%Y%m%d_%H%M%S")
    if output_format == "json":
        return f"duplicate_players_{current_dt}.json"
    elif output_format == "xlsx":
        return f"dup_players_{current_dt}.xlsx"
    elif output_format == "pdf":
        return f"duplicate_players_{current_dt}.pdf"
    else:
        raise ValueError("Unsupported output format")


class Command(BaseCommand):
    help = "Create a summary of missing player cards by team, output to json, google sheets, or pdf file"

    def add_arguments(self, parser):
        # Named argument/Option (Optional, with a default)
        parser.add_argument(
            "-o",
            "--output",
            type=str,
            required=True,  # Makes this flag mandatory
            help="The file path for the output",
        )
        parser.add_argument(
            "-f",
            "--format",
            type=str,
            choices=["json", "xlsx", "pdf"],
            default="json",
            help="The output format (json, xlsx, pdf)",
        )

    def handle(self, *args, **options):
        output_dir = options["output"]
        output_format = options["format"]
        file_name = get_file_name(output_format)
        output_path = Path(output_dir) / file_name
        write_dup_players_to_file(output_path)
        self.stdout.write(
            self.style.SUCCESS(f"Duplicate players summary written to {output_path}")
        )
