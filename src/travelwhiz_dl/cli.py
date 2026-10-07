"""CLI interface for the UK GTFS downloader."""

# # # # IMPORTS # # # #
# Built-Ins
import argparse

# # # # FUNCTIONS # # # #

# ---------------------------------------------------------------------------
# Command-line interface
# ---------------------------------------------------------------------------


def build_argument_parser() -> argparse.ArgumentParser:
    """Construct the command-line argument parser."""
    parser = argparse.ArgumentParser(
        description=(
            "Download a regional UK bus/metro GTFS feed and the "
            "GB-wide National Rail GTFS feed."
        )
    )

    parser.add_argument(
        "place_name",
        help=(
            "Place or region used to select the regional bus feed, "
            'for example "Greater Manchester".'
        ),
    )

    parser.add_argument(
        "output_directory",
        help=("Directory to which the GTFS ZIP files will be downloaded."),
    )

    parser.add_argument(
        "--bus-only",
        action="store_true",
        help="Download the regional bus feed without National Rail.",
    )

    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing GTFS ZIP files.",
    )

    parser.add_argument(
        "--no-validation",
        action="store_true",
        help="Do not perform basic GTFS ZIP validation.",
    )

    parser.add_argument(
        "--minimum-match-score",
        type=float,
        default=0.72,
        help=("Minimum fuzzy matching score between 0 and 1. Default: 0.72."),
    )

    return parser
