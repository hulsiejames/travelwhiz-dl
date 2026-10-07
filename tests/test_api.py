"""Tests for the public travelwhiz_dl API."""

from pathlib import Path

import pytest

from travelwhiz_dl import api
from travelwhiz_dl.models import GTFSFeed


@pytest.fixture
def north_west_feed() -> GTFSFeed:
    """Return a representative regional bus feed."""
    return GTFSFeed(
        name="North West England",
        url=("https://storage.example.com/uk-busmetro-NW.gtfs.zip"),
        category="regional_bus",
    )


@pytest.fixture
def national_rail_feed() -> GTFSFeed:
    """Return a representative National Rail feed."""
    return GTFSFeed(
        name="National Rail",
        url=("https://storage.example.com/gb-nationalrail.gtfs.zip"),
        category="national_rail",
    )


def test_download_uk_gtfs_downloads_bus_and_rail(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    north_west_feed: GTFSFeed,
    national_rail_feed: GTFSFeed,
) -> None:
    """The public API should download both requested feeds."""
    downloaded_bus_path = tmp_path / "uk-busmetro-NW.gtfs.zip"
    downloaded_rail_path = tmp_path / "gb-nationalrail.gtfs.zip"

    def fake_obtain_available_feeds() -> tuple[list[GTFSFeed], GTFSFeed]:
        return [north_west_feed], national_rail_feed

    expected_minimum_score = 0.72

    def fake_match_place_to_bus_feed(
        place_name: str,
        bus_feeds: list[GTFSFeed],
        minimum_score: float,
    ) -> tuple[GTFSFeed, float, str]:
        assert place_name == "Greater Manchester"
        assert bus_feeds == [north_west_feed]
        assert minimum_score == expected_minimum_score

        return (
            north_west_feed,
            1.0,
            "greater manchester",
        )

    download_calls: list[dict[str, object]] = []

    def fake_download_gtfs_feed(
        feed: GTFSFeed,
        output_directory: Path,
        *,
        overwrite: bool,
        validate: bool,
    ) -> Path:
        download_calls.append(
            {
                "feed": feed,
                "output_directory": output_directory,
                "overwrite": overwrite,
                "validate": validate,
            }
        )

        if feed == north_west_feed:
            return downloaded_bus_path

        if feed == national_rail_feed:
            return downloaded_rail_path

        raise AssertionError(f"Unexpected feed: {feed}")

    monkeypatch.setattr(
        api,
        "obtain_available_feeds",
        fake_obtain_available_feeds,
    )
    monkeypatch.setattr(
        api,
        "match_place_to_bus_feed",
        fake_match_place_to_bus_feed,
    )
    monkeypatch.setattr(
        api,
        "download_gtfs_feed",
        fake_download_gtfs_feed,
    )

    result = api.download_uk_gtfs(
        place_name="Greater Manchester",
        output_directory=tmp_path,
        include_national_rail=True,
        overwrite=False,
        validate=True,
        minimum_match_score=0.72,
    )

    assert result == {
        "bus": downloaded_bus_path,
        "rail": downloaded_rail_path,
    }

    assert download_calls == [
        {
            "feed": north_west_feed,
            "output_directory": tmp_path.resolve(),
            "overwrite": False,
            "validate": True,
        },
        {
            "feed": national_rail_feed,
            "output_directory": tmp_path.resolve(),
            "overwrite": False,
            "validate": True,
        },
    ]


def test_download_uk_gtfs_can_download_bus_only(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    north_west_feed: GTFSFeed,
    national_rail_feed: GTFSFeed,
) -> None:
    """National Rail should be omitted when it is not requested."""
    downloaded_bus_path = tmp_path / "uk-busmetro-NW.gtfs.zip"

    monkeypatch.setattr(
        api,
        "obtain_available_feeds",
        lambda: (
            [north_west_feed],
            national_rail_feed,
        ),
    )

    monkeypatch.setattr(
        api,
        "match_place_to_bus_feed",
        lambda **_kwargs: (
            north_west_feed,
            1.0,
            "greater manchester",
        ),
    )

    downloaded_feeds: list[GTFSFeed] = []

    def fake_download_gtfs_feed(
        feed: GTFSFeed,
        output_directory: Path,
        *,
        overwrite: bool,
        validate: bool,
    ) -> Path:
        del output_directory, overwrite, validate
        downloaded_feeds.append(feed)
        return downloaded_bus_path

    monkeypatch.setattr(
        api,
        "download_gtfs_feed",
        fake_download_gtfs_feed,
    )

    result = api.download_uk_gtfs(
        place_name="Manchester",
        output_directory=tmp_path,
        include_national_rail=False,
    )

    assert result == {
        "bus": downloaded_bus_path,
    }

    assert downloaded_feeds == [
        north_west_feed,
    ]


def test_download_uk_gtfs_passes_options_to_downloader(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    north_west_feed: GTFSFeed,
    national_rail_feed: GTFSFeed,
) -> None:
    """Overwrite and validation options should reach each download."""
    monkeypatch.setattr(
        api,
        "obtain_available_feeds",
        lambda: (
            [north_west_feed],
            national_rail_feed,
        ),
    )

    monkeypatch.setattr(
        api,
        "match_place_to_bus_feed",
        lambda **_kwargs: (
            north_west_feed,
            1.0,
            "greater manchester",
        ),
    )

    calls: list[tuple[GTFSFeed, Path, bool, bool]] = []

    def fake_download_gtfs_feed(
        feed: GTFSFeed,
        output_directory: Path,
        *,
        overwrite: bool,
        validate: bool,
    ) -> Path:
        calls.append(
            (
                feed,
                output_directory,
                overwrite,
                validate,
            )
        )

        return output_directory / feed.filename

    monkeypatch.setattr(
        api,
        "download_gtfs_feed",
        fake_download_gtfs_feed,
    )

    api.download_uk_gtfs(
        place_name="Greater Manchester",
        output_directory=tmp_path,
        include_national_rail=True,
        overwrite=True,
        validate=False,
    )

    assert calls == [
        (
            north_west_feed,
            tmp_path.resolve(),
            True,
            False,
        ),
        (
            national_rail_feed,
            tmp_path.resolve(),
            True,
            False,
        ),
    ]


def test_download_uk_gtfs_passes_match_threshold(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    north_west_feed: GTFSFeed,
    national_rail_feed: GTFSFeed,
) -> None:
    """The configured minimum score should reach the matcher."""
    received_arguments: dict[str, object] = {}

    monkeypatch.setattr(
        api,
        "obtain_available_feeds",
        lambda: (
            [north_west_feed],
            national_rail_feed,
        ),
    )

    def fake_match_place_to_bus_feed(
        place_name: str,
        bus_feeds: list[GTFSFeed],
        minimum_score: float,
    ) -> tuple[GTFSFeed, float, str]:
        received_arguments["place_name"] = place_name
        received_arguments["bus_feeds"] = bus_feeds
        received_arguments["minimum_score"] = minimum_score

        return (
            north_west_feed,
            0.85,
            "greater manchster",
        )

    monkeypatch.setattr(
        api,
        "match_place_to_bus_feed",
        fake_match_place_to_bus_feed,
    )

    monkeypatch.setattr(
        api,
        "download_gtfs_feed",
        lambda feed, output_directory, **_kwargs: output_directory / feed.filename,
    )

    api.download_uk_gtfs(
        place_name="Greater Manchster",
        output_directory=tmp_path,
        include_national_rail=False,
        minimum_match_score=0.80,
    )

    assert received_arguments == {
        "place_name": "Greater Manchster",
        "bus_feeds": [north_west_feed],
        "minimum_score": 0.80,
    }


def test_download_uk_gtfs_propagates_discovery_error(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A feed-discovery failure should not be hidden by the API."""

    def fake_obtain_available_feeds() -> tuple[list[GTFSFeed], GTFSFeed]:
        raise RuntimeError("README unavailable")

    monkeypatch.setattr(
        api,
        "obtain_available_feeds",
        fake_obtain_available_feeds,
    )

    with pytest.raises(
        RuntimeError,
        match="README unavailable",
    ):
        api.download_uk_gtfs(
            place_name="Manchester",
            output_directory=tmp_path,
        )


def test_download_uk_gtfs_propagates_match_error(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    north_west_feed: GTFSFeed,
    national_rail_feed: GTFSFeed,
) -> None:
    """An unrecognised place error should reach the caller."""
    monkeypatch.setattr(
        api,
        "obtain_available_feeds",
        lambda: (
            [north_west_feed],
            national_rail_feed,
        ),
    )

    def fake_match_place_to_bus_feed(**_kwargs: object) -> tuple[GTFSFeed, float, str]:
        raise ValueError("Could not confidently match place")

    monkeypatch.setattr(
        api,
        "match_place_to_bus_feed",
        fake_match_place_to_bus_feed,
    )

    with pytest.raises(
        ValueError,
        match="Could not confidently match place",
    ):
        api.download_uk_gtfs(
            place_name="Unknown Place",
            output_directory=tmp_path,
        )


def test_download_uk_gtfs_propagates_download_error(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    north_west_feed: GTFSFeed,
    national_rail_feed: GTFSFeed,
) -> None:
    """A failed download should reach the caller."""
    monkeypatch.setattr(
        api,
        "obtain_available_feeds",
        lambda: (
            [north_west_feed],
            national_rail_feed,
        ),
    )

    monkeypatch.setattr(
        api,
        "match_place_to_bus_feed",
        lambda **_kwargs: (
            north_west_feed,
            1.0,
            "manchester",
        ),
    )

    def fake_download_gtfs_feed(*_args: object, **_kwargs: object) -> Path:
        raise RuntimeError("HTTP 500 while downloading feed")

    monkeypatch.setattr(
        api,
        "download_gtfs_feed",
        fake_download_gtfs_feed,
    )

    with pytest.raises(
        RuntimeError,
        match="HTTP 500",
    ):
        api.download_uk_gtfs(
            place_name="Manchester",
            output_directory=tmp_path,
        )
