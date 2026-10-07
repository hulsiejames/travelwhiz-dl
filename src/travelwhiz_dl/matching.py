"""Match UK place names to regional TravelWhiz feeds."""

# # # # IMPORTS # # # #
# Built-Ins
from __future__ import annotations
import re
import unicodedata
from difflib import SequenceMatcher
from typing import Iterable

# Local
from travelwhiz_dl.config import DEFAULT_MINIMUM_MATCH_SCORE
from travelwhiz_dl.locations.lookups import PLACE_TO_REGION
from travelwhiz_dl.models import GTFSFeed

# # # # FUNCTIONS # # # #
def normalise_text(value: str) -> str:
    """Normalise text for place-name matching."""
    value = unicodedata.normalize("NFKD", value)
    value = value.encode("ascii", errors="ignore").decode("ascii")
    value = value.casefold()
    value = value.replace("&", " and ")
    value = re.sub(r"[^a-z0-9]+", " ", value)

    return " ".join(value.split())


def similarity(first: str, second: str) -> float:
    """Return a similarity score between zero and one."""
    return SequenceMatcher(
        None,
        normalise_text(first),
        normalise_text(second),
    ).ratio()


def find_feed_for_region(
    region_name: str,
    bus_feeds: Iterable[GTFSFeed],
) -> GTFSFeed | None:
    """Find an exact feed match using the canonical region name."""
    normalised_region = normalise_text(region_name)

    for feed in bus_feeds:
        if normalise_text(feed.name) == normalised_region:
            return feed

    return None


def match_place_to_bus_feed(
    place_name: str,
    bus_feeds: Iterable[GTFSFeed],
    minimum_score: float = DEFAULT_MINIMUM_MATCH_SCORE,
) -> tuple[GTFSFeed, float, str\]:
    """Match a supplied place name to a regional bus feed."""
    available_feeds = list(bus_feeds)

    if not available_feeds:
        raise ValueError("No bus feeds were supplied for matching.")

    cleaned_place = normalise_text(place_name)

    if not cleaned_place:
        raise ValueError("place_name cannot be empty.")

    exact_region = PLACE_TO_REGION.get(cleaned_place)

    if exact_region:
        exact_feed = find_feed_for_region(
            exact_region,
            available_feeds,
        )

        if exact_feed:
            return exact_feed, 1.0, cleaned_place

    for feed in available_feeds:
        if cleaned_place == normalise_text(feed.name):
            return feed, 1.0, feed.name

    containment_candidates: list[
        tuple[float, str, GTFSFeed]
    ] = []

    for alias, region_name in PLACE_TO_REGION.items():
        if alias in cleaned_place or cleaned_place in alias:
            feed = find_feed_for_region(
                region_name,
                available_feeds,
            )

            if feed:
                coverage = min(
                    len(alias),
                    len(cleaned_place),
                ) / max(
                    len(alias),
                    len(cleaned_place),
                )

                containment_candidates.append(
                    (coverage, alias, feed)
                )

    if containment_candidates:
        containment_candidates.sort(
            key=lambda item: item[0],
            reverse=True,
        )

        best_coverage, best_alias, best_feed = (
            containment_candidates[0]
        )

        if best_coverage >= 0.60:
            return best_feed, best_coverage, best_alias

    fuzzy_candidates: list[
        tuple[float, str, GTFSFeed]
    ] = []

    for alias, region_name in PLACE_TO_REGION.items():
        feed = find_feed_for_region(
            region_name,
            available_feeds,
        )

        if feed:
            fuzzy_candidates.append(
                (
                    similarity(cleaned_place, alias),
                    alias,
                    feed,
                )
            )

    for feed in available_feeds:
        fuzzy_candidates.append(
            (
                similarity(cleaned_place, feed.name),
                feed.name,
                feed,
            )
        )

    fuzzy_candidates.sort(
        key=lambda item: item[0],
        reverse=True,
    )

    best_score, best_term, best_feed = fuzzy_candidates[0]

    if best_score < minimum_score:
        suggestions = "\n".join(
            f"  - {term!r} -> {feed.name} "
            f"(score {score:.2f})"
            for score, term, feed in fuzzy_candidates[:5]
        )

        available_regions = ", ".join(
            feed.name for feed in available_feeds
        )

        raise ValueError(
            f"Could not confidently match {place_name!r} to a "
            f"regional GTFS feed.\n\n"
            f"Best possible matches were:\n"
            f"{suggestions}\n\n"
            f"Available feed regions:\n"
            f"{available_regions}\n\n"
            f"If the intended match is correct, add the place to "
            f"PLACE_TO_REGION or reduce minimum_score."
        )

    return best_feed, best_score, best_term
``