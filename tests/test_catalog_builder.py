from gdi_catalog_builder.converters.catalog_builder import CatalogBuilder


def test_build_catalog_from_csv():
    catalog = CatalogBuilder.from_csv(
        "input/sample_datasets.csv"
    )

    assert catalog.title == "Norwegian GDI Catalog"
    assert len(catalog.datasets) == 1

    dataset = catalog.datasets[0]

    assert dataset.identifier == "GDI-NO-UIO-001"
    assert dataset.title == "Norwegian Cancer Dataset"
    assert dataset.creators[0].name == "University of Oslo"

    assert dataset.publisher is not None
    assert dataset.publisher.name == "ELIXIR Norway"

    assert dataset.keyword == ["cancer", "genomics"]
