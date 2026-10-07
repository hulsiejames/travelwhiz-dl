from travelwhiz_dl.discovery import extract_gtfs_urls


def test_extract_gtfs_urls_removes_duplicates():
    readme = """
    https://example.com/uk-busmetro-NW.gtfs.zip
    https://example.com/gb-nationalrail.gtfs.zip
    https://example.com/uk-busmetro-NW.gtfs.zip
    """

    urls = extract_gtfs_urls(readme)

    assert urls == [
        "https://example.com/uk-busmetro-NW.gtfs.zip",
        "https://example.com/gb-nationalrail.gtfs.zip",
    ]
