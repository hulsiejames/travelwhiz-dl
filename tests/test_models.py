"""Tests for travelwhiz_dl.models."""

from dataclasses import FrozenInstanceError

import pytest

from travelwhiz_dl.models import GTFSFeed


def test_gtfs_feed_stores_supplied_values() -> None:
    """A GTFSFeed should retain its supplied metadata."""
    feed = GTFSFeed(
        name="North West England",
        url=("https://storage.example.com/uk-busmetro-NW.gtfs.zip"),
        category="regional_bus",
    )

    assert feed.name == "North West England"
    assert feed.url == ("https://storage.example.com/uk-busmetro-NW.gtfs.zip")
    assert feed.category == "regional_bus"


def test_gtfs_feed_filename_is_extracted_from_url() -> None:
    """The filename property should return the URL's final component."""
    feed = GTFSFeed(
        name="National Rail",
        url=("https://storage.example.com/generated-gtfs/gb-nationalrail.gtfs.zip"),
        category="national_rail",
    )

    assert feed.filename == "gb-nationalrail.gtfs.zip"


def test_gtfs_feed_filename_handles_simple_url() -> None:
    """The filename property should also work without nested URL paths."""
    feed = GTFSFeed(
        name="Test Feed",
        url="https://example.com/test.gtfs.zip",
        category="test",
    )

    assert feed.filename == "test.gtfs.zip"


def test_gtfs_feed_is_immutable() -> None:
    """GTFSFeed instances should not be mutable."""
    feed = GTFSFeed(
        name="North West England",
        url="https://example.com/north-west.gtfs.zip",
        category="regional_bus",
    )

    with pytest.raises(FrozenInstanceError):
        feed.name = "East Midlands"


def test_equal_gtfs_feeds_compare_as_equal() -> None:
    """Equivalent GTFSFeed objects should compare by value."""
    first_feed = GTFSFeed(
        name="National Rail",
        url="https://example.com/rail.gtfs.zip",
        category="national_rail",
    )

    second_feed = GTFSFeed(
        name="National Rail",
        url="https://example.com/rail.gtfs.zip",
        category="national_rail",
    )

    assert first_feed == second_feed


def test_different_gtfs_feeds_do_not_compare_as_equal() -> None:
    """Feeds with differing values should not compare as equal."""
    bus_feed = GTFSFeed(
        name="North West England",
        url="https://example.com/bus.gtfs.zip",
        category="regional_bus",
    )

    rail_feed = GTFSFeed(
        name="National Rail",
        url="https://example.com/rail.gtfs.zip",
        category="national_rail",
    )

    assert bus_feed != rail_feed
