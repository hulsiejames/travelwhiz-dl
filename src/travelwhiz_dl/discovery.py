"""Discover currently available TravelWhiz GTFS feeds."""

# # # # IMPORTS # # # #
# Built-Ins
from __future__ import annotations

import re
import urllib.error
import urllib.request

# Local
from travelwhiz_dl.config import (
    DEFAULT_README_TIMEOUT,
    GITHUB_README_URL,
    USER_AGENT,
)
from travelwhiz_dl.lookups import REGION_CODE_TO_NAME
from travelwhiz_dl.models import GTFSFeed

# # # # CONSTANTS # # # #

_BUS_FILENAME_PATTERN = re.compile(
    r"^uk-busmetro-(?P<region>.+)\.gtfs\.zip$",
    flags=re.IGNORECASE,
)

_GTFS_URL_PATTERN = re.compile(
    r"https?://[^\s)>\"']+?\.gtfs\.zip",
    flags=re.IGNORECASE,
)


def fetch_readme(
    readme_url: str = GITHUB_README_URL,
    timeout: int = DEFAULT_README_TIMEOUT,
) -> str:
    """Download the current repository README."""
    request = urllib.request.Request(  # noqa: S310
        readme_url,
        headers={"User-Agent": USER_AGENT},
    )

    try:
        with urllib.request.urlopen(  # noqa: S310
            request,
            timeout=timeout,
        ) as response:
            encoding = response.headers.get_content_charset() or "utf-8"
            return response.read().decode(encoding)

    except urllib.error.HTTPError as exc:
        raise RuntimeError(
            f"GitHub returned HTTP {exc.code} while downloading "
            f"the repository README: {readme_url}"
        ) from exc

    except urllib.error.URLError as exc:
        raise RuntimeError(
            f"Could not download the repository README. Network error: {exc.reason}"
        ) from exc


def extract_gtfs_urls(readme_text: str) -> list[str]:
    """Extract unique GTFS ZIP URLs from README text."""
    discovered_urls = [
        match.rstrip(".,;:") for match in _GTFS_URL_PATTERN.findall(readme_text)
    ]

    unique_urls = list(dict.fromkeys(discovered_urls))

    if not unique_urls:
        raise RuntimeError(
            "No .gtfs.zip download URLs were found in the repository "
            "README. The README format or filenames may have changed."
        )

    return unique_urls


def obtain_available_feeds(
    readme_url: str = GITHUB_README_URL,
) -> tuple[list[GTFSFeed], GTFSFeed]:
    """Obtain regional bus feeds and the National Rail feed."""
    readme_text = fetch_readme(readme_url)
    gtfs_urls = extract_gtfs_urls(readme_text)

    bus_feeds: list[GTFSFeed] = []
    rail_candidates: list[GTFSFeed] = []

    for url in gtfs_urls:
        filename = url.rsplit("/", 1)[-1]
        bus_match = _BUS_FILENAME_PATTERN.match(filename)

        if bus_match:
            region_code = bus_match.group("region").upper()

            region_name = REGION_CODE_TO_NAME.get(
                region_code,
                region_code.replace("-", " ").title(),
            )

            bus_feeds.append(
                GTFSFeed(
                    name=region_name,
                    url=url,
                    category="regional_bus",
                )
            )

        if filename.casefold() == "gb-nationalrail.gtfs.zip":
            rail_candidates.append(
                GTFSFeed(
                    name="National Rail",
                    url=url,
                    category="national_rail",
                )
            )

    if not bus_feeds:
        raise RuntimeError(
            "The README was downloaded, but no regional "
            "uk-busmetro-*.gtfs.zip feeds were found."
        )

    if not rail_candidates:
        raise RuntimeError(
            "The README was downloaded, but gb-nationalrail.gtfs.zip was not found."
        )

    if len(rail_candidates) > 1:
        raise RuntimeError(
            "More than one National Rail feed URL was found. "
            "The repository structure may have changed."
        )

    bus_feeds.sort(key=lambda feed: feed.name)

    return bus_feeds, rail_candidates[0]
