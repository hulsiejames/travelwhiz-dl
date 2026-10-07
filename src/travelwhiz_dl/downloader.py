"""Download GTFS feeds safely."""

# # # # IMPORTS # # # #
# Built-Ins
from __future__ import annotations
import shutil
import urllib.error
import urllib.request
from pathlib import Path

# Local
from travelwhiz_dl.config import (
    DEFAULT_CHUNK_SIZE,
    DEFAULT_DOWNLOAD_TIMEOUT,
    USER_AGENT,
)
from travelwhiz_dl.models import GTFSFeed
from travelwhiz_dl.validation import validate_gtfs_zip


# # # # FUNCTIONS # # # #

def format_megabytes(number_of_bytes: int) -> str:
    """Format a byte count as mebibytes."""
    return f"{number_of_bytes / (1024 * 1024):,.1f} MiB"


def download_gtfs_feed(
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
    temporary_destination = destination.with_name(
        destination.name + ".part"
    )

    if destination.exists() and not overwrite:
        if not validate:
            print(f"[SKIP] Existing file found: {destination}")
            return destination

        try:
            validate_gtfs_zip(destination)
        except RuntimeError:
            print(
                "[WARNING] Existing file failed validation and "
                "will be downloaded again."
            )
        else:
            print(
                f"[SKIP] Existing valid file found: {destination}"
            )
            return destination

    temporary_destination.unlink(missing_ok=True)

    request = urllib.request.Request(
        feed.url,
        headers={"User-Agent": USER_AGENT},
    )

    print()
    print(f"[DOWNLOAD] {feed.name}")
    print(f"URL:         {feed.url}")
    print(f"Destination: {destination}")

    try:
        with urllib.request.urlopen(
            request,
            timeout=timeout,
        ) as response:
            content_length = response.headers.get("Content-Length")
            total_size = (
                int(content_length)
                if content_length is not None
                else None
            )

            downloaded_size = 0
            last_reported_percentage = -10

            with temporary_destination.open("wb") as output_file:
                while chunk := response.read(chunk_size):
                    output_file.write(chunk)
                    downloaded_size += len(chunk)

                    if total_size:
                        percentage = int(
                            downloaded_size * 100 / total_size
                        )
                        report_percentage = percentage // 10 * 10

                        if (
                            report_percentage
                            > last_reported_percentage
                        ):
                            print(
                                f"Progress:    {percentage:3d}% "
                                f"({format_megabytes(downloaded_size)} "
                                f"of {format_megabytes(total_size)})"
                            )
                            last_reported_percentage = (
                                report_percentage
                            )

        if validate:
            print(f"[VALIDATE] {temporary_destination.name}")
            validate_gtfs_zip(temporary_destination)

        temporary_destination.replace(destination)

    except urllib.error.HTTPError as exc:
        temporary_destination.unlink(missing_ok=True)

        raise RuntimeError(
            f"HTTP {exc.code} while downloading {feed.name}: "
            f"{feed.url}"
        ) from exc

    except urllib.error.URLError as exc:
        temporary_destination.unlink(missing_ok=True)

        raise RuntimeError(
            f"Network error while downloading {feed.name}: "
            f"{exc.reason}"
        ) from exc

    except Exception:
        temporary_destination.unlink(missing_ok=True)
        raise

    print(f"[COMPLETE] {destination}")

    return destination
