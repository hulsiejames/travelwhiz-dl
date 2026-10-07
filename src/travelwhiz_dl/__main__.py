"""Command-line entry point for travelwhiz_dl."""

# # # #IMPORTS # # # #
# Built-Ins
from __future__ import annotations
import sys

# Local
from travelwhiz_dl.api import download_uk_gtfs
from travelwhiz_dl.arguments.cli import build_argument_parser


# # # # FUNCTIONS # # # #
def command_line_main() -> int:
    """Run the travelwhiz-dl command-line interface."""
    parser = build_argument_parser()
    arguments = parser.parse_args()

    if not 0.0 <= arguments.minimum_match_score <= 1.0:
        parser.error(
            "--minimum-match-score must be between 0 and 1."
        )

    try:
        download_uk_gtfs(
            place_name=arguments.place_name,
            output_directory=arguments.output_directory,
            include_national_rail=not arguments.bus_only,
            overwrite=arguments.overwrite,
            validate=not arguments.no_validation,
            minimum_match_score=arguments.minimum_match_score,
        )

    except KeyboardInterrupt:
        print(
            "\nDownload cancelled by the user.",
            file=sys.stderr,
        )
        return 130

    except Exception as exc:
        print(
            f"\nERROR: {exc}",
            file=sys.stderr,
        )
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(command_line_main())