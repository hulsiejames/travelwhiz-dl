"""Data models used by travelwhiz_dl."""

# # # # IMPORTS # # # #
# Built-Ins
from __future__ import annotations
from dataclasses import dataclass


# # # # DATA CLASSES # # # #

@dataclass(frozen=True, slots=True)
class GTFSFeed:
    """Description of one downloadable GTFS feed."""

    name: str
    url: str
    category: str

    @property
    def filename(self) -> str:
        """Return the final component of the download URL."""
        return self.url.rsplit("/", 1)[-1]