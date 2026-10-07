"""Package configuration constants."""

# # # # CONSTANTS # # # #
GITHUB_README_URL = (
    r"https://raw.githubusercontent.com/"
    r"travelwhiz-ltd/GB-Bus-Train-Metro-GTFS/"
    r"main/README.md"
)

USER_AGENT = (
    r"Mozilla/5.0 "
    r"(compatible; travelwhiz-dl/1.0; "
    r"+https://github.com/travelwhiz-ltd/GB-Bus-Train-Metro-GTFS)"
)

DEFAULT_README_TIMEOUT = 60
DEFAULT_DOWNLOAD_TIMEOUT = 300
DEFAULT_CHUNK_SIZE = 1024 * 1024
DEFAULT_MINIMUM_MATCH_SCORE = 0.72

REQUIRED_GTFS_FILES = frozenset(
    {
        "agency.txt",
        "routes.txt",
        "trips.txt",
        "stops.txt",
        "stop_times.txt",
    }
)
