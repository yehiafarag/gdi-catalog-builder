from gdi_catalog_builder.models.agent import Agent
from gdi_catalog_builder.models.catalog import Catalog
from gdi_catalog_builder.models.dataset import DatasetMetadata
from gdi_catalog_builder.models.distribution import Distribution


def test_catalog_builds_with_package_imports():
    catalog = Catalog(
        title="Norwegian GDI Catalog",
        datasets=[
            DatasetMetadata(
                title="Cancer Dataset",
                creators=[Agent(name="University of Oslo")],
                publisher=Agent(name="ELIXIR Norway"),
                distributions=[
                    Distribution(
                        title="Dataset Access",
                        access_url="https://example.org/access",
                    )
                ],
            )
        ],
    )

    assert catalog.title == "Norwegian GDI Catalog"
    assert catalog.datasets[0].title == "Cancer Dataset"
    assert catalog.datasets[0].publisher.name == "ELIXIR Norway"
