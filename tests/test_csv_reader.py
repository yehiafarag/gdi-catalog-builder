from gdi_catalog_builder.converters.csv_reader import CSVReader


def test_read_sample_datasets():
    rows = CSVReader.read(
        "input/sample_datasets.csv"
    )

    assert len(rows) == 1

    dataset = rows[0]

    assert dataset["id"] == "GDI-NO-UIO-001"
    assert dataset["name"] == "Norwegian Cancer Dataset"
    assert dataset["author_name"] == "University of Oslo"
    assert dataset["publisher_name"] == "ELIXIR Norway"