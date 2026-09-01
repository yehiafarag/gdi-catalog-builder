from gdi_catalog_builder.converters.csv_reader import CSVReader
from gdi_catalog_builder.converters.dataset_mapper import DatasetMapper


def test_map_csv_row_to_dataset():
    rows = CSVReader.read(
        "input/sample_datasets.csv"
    )

    assert len(rows) == 1

    dataset = DatasetMapper.from_csv_row(rows[0])

    # id
    assert dataset.identifier == "GDI-NO-UIO-001"

    # name
    assert dataset.title == "Norwegian Cancer Dataset"

    # description
    assert (
            dataset.description
            == "A test dataset for GDI validation"
    )

    # author_name and author_id
    assert len(dataset.creators) == 1
    assert dataset.creators[0].name == "University of Oslo"
    assert dataset.creators[0].identifier == "UIO"

    # keywords
    assert dataset.keyword == [
        "cancer",
        "genomics",
    ]

    # publisher_name and publisher_id
    assert dataset.publisher is not None
    assert dataset.publisher.name == "ELIXIR Norway"
    assert dataset.publisher.identifier == "ELIXIR-NO"

    # theme
    assert dataset.theme == [
        (
            "http://publications.europa.eu/"
            "resource/authority/data-theme/HEAL"
        )
    ]

    # contact_point
    assert len(dataset.publisher.contact_points) == 1

    contact_point = dataset.publisher.contact_points[0]

    assert (
            contact_point.email
            == "mailto:gdi-contact@elixir.no"
    )
    assert contact_point.url is None

    # issued
    assert dataset.issued == "2026-09-01"

    # external_link
    assert dataset.is_referenced_by == [
        "https://example.no/datasets/GDI-NO-UIO-001"
    ]

    # access_rights
    assert dataset.access_rights == (
        "http://publications.europa.eu/"
        "resource/authority/access-right/RESTRICTED"
    )

    # applicable_legislation
    assert dataset.applicable_legislation == [
        "http://data.europa.eu/eli/reg/2025/327/oj"
    ]

    # health_category
    assert dataset.health_category == [
        (
            "http://data.gdi.eu/core/p2/"
            "HealthCategoryHumanGenomic"
        )
    ]