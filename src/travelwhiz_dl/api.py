"""Public programmatic interface for travelwhiz_dl."""

# # # # IMPORTS # # # #
# Built-Ins
from __future__ import annotations

import logging
from pathlib import Path

# Local
from travelwhiz_dl.config import DEFAULT_MINIMUM_MATCH_SCORE
from travelwhiz_dl.discovery import obtain_available_feeds
from travelwhiz_dl.downloader import download_gtfs_feed
from travelwhiz_dl.matching import match_place_to_bus_feed

LOG = logging.getLogger(__name__)

# # # # FUNCTIONS # # # #


def download_uk_gtfs(
    place_name: str,
    output_directory: str | Path,
    *,
    include_national_rail: bool = True,
    overwrite: bool = False,
    validate: bool = True,
    minimum_match_score: float = DEFAULT_MINIMUM_MATCH_SCORE,
) -> dict[str, Path]:
    """
    Download regional bus/metro GTFS and National Rail GTFS.

    Parameters
    ----------
    place_name
        Place or regional name used to select the bus/metro feed.

    output_directory
        Directory to which the GTFS ZIP files are downloaded.

    include_national_rail
        Whether to download the GB-wide National Rail feed.

    overwrite
        Whether existing files should be replaced.

    validate
        Whether downloaded and existing files should be validated.

    minimum_match_score
        Minimum accepted fuzzy matching score.

    Returns
    -------
    dict[str, pathlib.Path]
        Paths to the downloaded bus and, when requested, rail files.
    """
    output_directory = Path(output_directory).expanduser().resolve()

    LOG.info("%s", "=" * 72)
    LOG.info("UK GTFS downloader")
    LOG.info("%s", "=" * 72)
    LOG.info("Requested place:  %s", place_name)
    LOG.info("Output directory: %s", output_directory)
    LOG.info("[DISCOVERY] Reading current download URLs from GitHub...")

    bus_feeds, national_rail_feed = obtain_available_feeds()

    LOG.info("Found %s regional bus/metro feeds.", len(bus_feeds))
    LOG.info("Regional feeds: %s", ", ".join(feed.name for feed in bus_feeds))
    LOG.info("National Rail: %s", national_rail_feed.filename)

    selected_bus_feed, score, matched_term = match_place_to_bus_feed(
        place_name=place_name,
        bus_feeds=bus_feeds,
        minimum_score=minimum_match_score,
    )

    LOG.info("[MATCH]")
    LOG.info("Input:         %s", place_name)
    LOG.info("Matched term:  %s", matched_term)
    LOG.info("Selected feed: %s", selected_bus_feed.name)
    LOG.info("Match score:   %.2f", score)
    LOG.info("Bus filename:  %s", selected_bus_feed.filename)

    downloaded_files: dict[str, Path] = {}

    downloaded_files["bus"] = download_gtfs_feed(
        feed=selected_bus_feed,
        output_directory=output_directory,
        overwrite=overwrite,
        validate=validate,
    )

    if include_national_rail:
        downloaded_files["rail"] = download_gtfs_feed(
            feed=national_rail_feed,
            output_directory=output_directory,
            overwrite=overwrite,
            validate=validate,
        )

    LOG.info("%s", "=" * 72)
    LOG.info("Download summary")
    LOG.info("%s", "=" * 72)

    for category, downloaded_path in downloaded_files.items():
        LOG.info("%s: %s", category.title().ljust(8), downloaded_path)

    return downloaded_files
