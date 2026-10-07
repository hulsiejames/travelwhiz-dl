import zipfile

from travelwhiz_dl.validation import validate_gtfs_zip


def test_valid_gtfs_zip_passes(tmp_path):
    zip_path = tmp_path / "test.gtfs.zip"

    required_files = [
        "agency.txt",
        "routes.txt",
        "trips.txt",
        "stops.txt",
        "stop_times.txt",
    ]

    with zipfile.ZipFile(zip_path, mode="w") as archive:
        for filename in required_files:
            archive.writestr(filename, "")

    validate_gtfs_zip(zip_path)
