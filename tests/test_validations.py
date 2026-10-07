"""Tests for travelwhiz_dl.validation."""

import zipfile

from pathlib import Path

import pytest

from travelwhiz_dl.validation import (
    read_gtfs_members,
    validate_gtfs_zip,
)


REQUIRED_GTFS_FILES = {
    "agency.txt",
    "routes.txt",
    "trips.txt",
    "stops.txt",
    "stop_times.txt",
}


def create_gtfs_zip(
    zip_path: Path,
    filenames: set[str],
) -> Path:
    """
    Create a small GTFS-like ZIP for testing.

    Parameters
    ----------
    zip_path
        Path at which the test archive should be created.

    filenames
        File names to add to the archive.
    """
    with zipfile.ZipFile(zip_path, mode="w") as archive:
        for filename in filenames:
            archive.writestr(filename, "")

    return zip_path


def test_read_gtfs_members_returns_member_basenames(tmp_path):
    """ZIP members should be returned as lowercase basenames."""
    zip_path = create_gtfs_zip(
        tmp_path / "test.gtfs.zip",
        {
            "nested/directory/AGENCY.TXT",
            "nested/directory/routes.txt",
        },
    )

    members = read_gtfs_members(zip_path)

    assert members == {
        "agency.txt",
        "routes.txt",
    }


def test_validate_gtfs_zip_accepts_required_files(tmp_path):
    """A ZIP containing the required GTFS files should pass."""
    zip_path = create_gtfs_zip(
        tmp_path / "valid.gtfs.zip",
        REQUIRED_GTFS_FILES,
    )

    result = validate_gtfs_zip(zip_path)

    assert result is None


def test_validate_gtfs_zip_accepts_additional_files(tmp_path):
    """Optional and extended GTFS files should not cause failure."""
    zip_path = create_gtfs_zip(
        tmp_path / "valid-with-extras.gtfs.zip",
        REQUIRED_GTFS_FILES
        | {
            "calendar.txt",
            "calendar_dates.txt",
            "shapes.txt",
            "feed_info.txt",
        },
    )

    validate_gtfs_zip(zip_path)


def test_validate_gtfs_zip_accepts_nested_files(tmp_path):
    """
    Required files should be recognised even inside a ZIP directory.

    Although root-level GTFS files are preferable, read_gtfs_members uses
    each member's basename, so this documents the current behaviour.
    """
    nested_files = {
        f"gtfs/{filename}"
        for filename in REQUIRED_GTFS_FILES
    }

    zip_path = create_gtfs_zip(
        tmp_path / "nested.gtfs.zip",
        nested_files,
    )

    validate_gtfs_zip(zip_path)


def test_validate_gtfs_zip_is_case_insensitive(tmp_path):
    """Required filenames should be matched case-insensitively."""
    uppercase_files = {
        filename.upper()
        for filename in REQUIRED_GTFS_FILES
    }

    zip_path = create_gtfs_zip(
        tmp_path / "uppercase.gtfs.zip",
        uppercase_files,
    )

    validate_gtfs_zip(zip_path)


def test_validate_gtfs_zip_rejects_missing_required_file(
    tmp_path,
):
    """Validation should identify absent required GTFS files."""
    zip_path = create_gtfs_zip(
        tmp_path / "missing-stops.gtfs.zip",
        REQUIRED_GTFS_FILES - {"stops.txt"},
    )

    with pytest.raises(
        RuntimeError,
        match=r"Missing files: stops\.txt",
    ):
        validate_gtfs_zip(zip_path)


def test_validate_gtfs_zip_reports_multiple_missing_files(
    tmp_path,
):
    """Validation should report every missing required file."""
    zip_path = create_gtfs_zip(
        tmp_path / "incomplete.gtfs.zip",
        {
            "agency.txt",
            "routes.txt",
        },
    )

    with pytest.raises(RuntimeError) as exc_info:
        validate_gtfs_zip(zip_path)

    error_message = str(exc_info.value)

    assert "stops.txt" in error_message
    assert "stop_times.txt" in error_message
    assert "trips.txt" in error_message


def test_validate_gtfs_zip_rejects_non_zip_file(tmp_path):
    """A regular text file should not pass ZIP validation."""
    invalid_path = tmp_path / "not-a-zip.gtfs.zip"
    invalid_path.write_text(
        "This is not a ZIP archive.",
        encoding="utf-8",
    )

    with pytest.raises(
        RuntimeError,
        match="not a valid ZIP",
    ):
        validate_gtfs_zip(invalid_path)


def test_validate_gtfs_zip_rejects_missing_path(tmp_path):
    """A nonexistent path should raise an appropriate file error."""
    missing_path = tmp_path / "does-not-exist.gtfs.zip"

    with pytest.raises(FileNotFoundError):
        validate_gtfs_zip(missing_path)
