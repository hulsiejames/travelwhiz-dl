"""automated python downloads of travelwhiz curated feeds."""

from travelwhiz_dl.api import download_uk_gtfs
from travelwhiz_dl.models import GTFSFeed

from ._version import __version__

__all__ = [
    "GTFSFeed",
    "download_uk_gtfs",
]
