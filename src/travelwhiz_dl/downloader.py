"""Download GTFS feeds safely."""

# # # # IMPORTS # # # #
# Built-Ins
from __future__ import annotations

import logging
import urllib.error
import urllib.request
from pathlib import Path
from typing import TYPE_CHECKING

# Local
from travelwhiz_dl.config import (
    DEFAULT_CHUNK_SIZE,
    DEFAULT_DOWNLOAD_TIMEOUT,
    USER_AGENT,
)
from travelwhiz_dl.validation import validate_gtfs_zip

if TYPE_CHECKING:
    from travelwhiz_dl.models import GTFSFeed

LOG = logging.getLogger(__name__)

# # # # FUNCTIONS # # # #


def format_megabytes(number_of_bytes: int) -> str:
    """Format a byte count as mebibytes."""
    return f"{number_of_bytes / (1024 * 1024):,.1f} MiB"


def download_gtfs_feed(  # noqa: C901
    feed: GTFSFeed,
    output_directory: str | Path,
    *,
    overwrite: bool = False,
    validate: bool = True,
    timeout: int = DEFAULT_DOWNLOAD_TIMEOUT,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
) -> Path:
    """Download one GTFS feed using a temporary partial file."""
    output_directory = Path(output_directory).expanduser().resolve()
    output_directory.mkdir(parents=True, exist_ok=True)

    destination = output_directory / feed.filename
    temporary_destination = destination.with_name(destination.name + ".part")

    if destination.exists() and not overwrite:
        if not validate:
            LOG.info("[SKIP] Existing file found: %s", destination)
            return destination

        try:
            validate_gtfs_zip(destination)
        except RuntimeError:
            LOG.warning("Existing file failed validation and will be downloaded again.")
        else:
            LOG.info("[SKIP] Existing valid file found: %s", destination)
            return destination

    temporary_destination.unlink(missing_ok=True)

    request = urllib.request.Request(  # noqa: S310
        feed.url,
        headers={"User-Agent": USER_AGENT},
    )

    LOG.info("[DOWNLOAD] %s", feed.name)
    LOG.info("URL:         %s", feed.url)
    LOG.info("Destination: %s", destination)

    try:
        with urllib.request.urlopen(  # noqa: S310
            request,
            timeout=timeout,
        ) as response:
            content_length = response.headers.get("Content-Length")
            total_size = int(content_length) if content_length is not None else None

            downloaded_size = 0
            last_reported_percentage = -10

            with temporary_destination.open("wb") as output_file:
                while chunk := response.read(chunk_size):
                    output_file.write(chunk)
                    downloaded_size += len(chunk)

                    if total_size:
                        percentage = int(downloaded_size * 100 / total_size)
                        report_percentage = percentage // 10 * 10

                        if report_percentage > last_reported_percentage:
                            LOG.info(
                                "Progress:    %3d%% (%s of %s)",
                                percentage,
                                format_megabytes(downloaded_size),
                                format_megabytes(total_size),
                            )
                            last_reported_percentage = report_percentage

        if validate:
            LOG.info("[VALIDATE] %s", temporary_destination.name)
            validate_gtfs_zip(temporary_destination)

        temporary_destination.replace(destination)

    except urllib.error.HTTPError as exc:
        temporary_destination.unlink(missing_ok=True)

        raise RuntimeError(
            f"HTTP {exc.code} while downloading {feed.name}: {feed.url}"
        ) from exc

    except urllib.error.URLError as exc:
        temporary_destination.unlink(missing_ok=True)

        raise RuntimeError(
            f"Network error while downloading {feed.name}: {exc.reason}"
        ) from exc

    except Exception:
        temporary_destination.unlink(missing_ok=True)
        raise

    LOG.info("[COMPLETE] %s", destination)

    return destination
