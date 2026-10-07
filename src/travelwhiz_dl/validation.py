"""Basic GTFS ZIP validation."""

# # # # IMPORTS # # # #
# Built-Ins
from __future__ import annotations

import zipfile
from pathlib import Path

# Local
from travelwhiz_dl.config import REQUIRED_GTFS_FILES

# # # # FUNCTIONS # # # #


def read_gtfs_members(zip_path: Path) -> set[str]:
    """Return lowercase file basenames contained in a GTFS ZIP."""
    try:
        with zipfile.ZipFile(zip_path, mode="r") as archive:
            corrupt_member = archive.testzip()

            if corrupt_member is not None:
                raise RuntimeError(f"The ZIP contains a corrupt member: {corrupt_member}")

            return {
                Path(member).name.casefold()
                for member in archive.namelist()
                if not member.endswith("/")
            }

    except zipfile.BadZipFile as exc:
        raise RuntimeError(f"The downloaded file is not a valid ZIP: {zip_path}") from exc


def validate_gtfs_zip(zip_path: str | Path) -> None:
    """Check that a ZIP contains the principal required GTFS files."""
    zip_path = Path(zip_path)
    members = read_gtfs_members(zip_path)
    missing_files = REQUIRED_GTFS_FILES - members

    if missing_files:
        missing_text = ", ".join(sorted(missing_files))

        raise RuntimeError(
            f"The archive {zip_path.name!r} does not look like a "
            f"complete GTFS feed. Missing files: {missing_text}"
        )
