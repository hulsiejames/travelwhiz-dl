from travelwhiz_dl.matching import match_place_to_bus_feed
from travelwhiz_dl.models import GTFSFeed

BUS_FEEDS = [
    GTFSFeed(
        name="North West England",
        url=("https://example.com/uk-busmetro-NW.gtfs.zip"),
        category="regional_bus",
    ),
    GTFSFeed(
        name="East Midlands",
        url=("https://example.com/uk-busmetro-EM.gtfs.zip"),
        category="regional_bus",
    ),
]


def test_matches_greater_manchester_to_north_west():
    feed, score, matched_term = match_place_to_bus_feed(
        "Greater Manchester",
        BUS_FEEDS,
    )

    assert feed.name == "North West England"
    assert score == 1.0
    assert matched_term == "greater manchester"


def test_matches_leicester_to_east_midlands():
    feed, score, _ = match_place_to_bus_feed(
        "Leicester",
        BUS_FEEDS,
    )

    assert feed.name == "East Midlands"
    assert score == 1.0
