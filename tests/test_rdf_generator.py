from gdi_catalog_builder.converters.rdf_generator import RDFGenerator
from gdi_catalog_builder.models.catalog import Catalog

from gdi_catalog_builder.converters.rdf_generator import RDFGenerator
from gdi_catalog_builder.models.catalog import Catalog
from gdi_catalog_builder.models.dataset import DatasetMetadata


from gdi_catalog_builder.converters.rdf_generator import RDFGenerator
from gdi_catalog_builder.models.catalog import Catalog
from gdi_catalog_builder.models.dataset import DatasetMetadata
from gdi_catalog_builder.models.distribution import Distribution

from gdi_catalog_builder.converters.rdf_generator import RDFGenerator
from gdi_catalog_builder.models.agent import Agent
from gdi_catalog_builder.models.catalog import Catalog
from gdi_catalog_builder.models.dataset import DatasetMetadata


def test_catalog_graph_creation():
    catalog = Catalog(
        title="Norwegian GDI Catalog",
        description="Catalog for Norway"
    )

    graph = RDFGenerator().generate_catalog_graph(catalog)

    assert graph is not None
    assert len(graph) > 0






def test_catalog_graph_creation():
    catalog = Catalog(
        title="Norwegian GDI Catalog",
        description="Catalog for Norway"
    )

    graph = RDFGenerator().generate_catalog_graph(catalog)

    assert graph is not None
    assert len(graph) > 0


def test_catalog_with_dataset():
    catalog = Catalog(
        title="Norwegian GDI Catalog",
        datasets=[
            DatasetMetadata(
                title="Cancer Dataset",
                description="Registry dataset"
            )
        ]
    )

    graph = RDFGenerator().generate_catalog_graph(catalog)

    assert len(graph) > 3






def test_dataset_distribution_graph():

    catalog = Catalog(
        title="Norwegian GDI Catalog",
        datasets=[
            DatasetMetadata(
                title="Cancer Dataset",
                distributions=[
                    Distribution(
                        title="Access Endpoint",
                        access_url="https://example.no/access"
                    )
                ]
            )
        ]
    )

    graph = RDFGenerator().generate_catalog_graph(catalog)

    assert len(graph) > 5




def test_dataset_creator_publisher():

    catalog = Catalog(
        title="Norwegian GDI Catalog",
        datasets=[
            DatasetMetadata(
                title="Cancer Dataset",
                creators=[
                    Agent(name="University of Oslo")
                ],
                publisher=Agent(
                    name="ELIXIR Norway"
                )
            )
        ]
    )

    graph = RDFGenerator().generate_catalog_graph(catalog)

    assert len(graph) > 5

from gdi_catalog_builder.converters.rdf_generator import RDFGenerator
from gdi_catalog_builder.models.catalog import Catalog
from gdi_catalog_builder.models.dataset import DatasetMetadata
from gdi_catalog_builder.models.identifier import Identifier


def test_dataset_identifier():

    catalog = Catalog(
        title="Norwegian GDI Catalog",
        datasets=[
            DatasetMetadata(
                title="Cancer Dataset",
                identifiers=[
                    Identifier(
                        notation="NO-CANCER-001",
                        schema_agency="ELIXIR-NO",
                        name="Primary Dataset Identifier"
                    )
                ]
            )
        ]
    )

    graph = RDFGenerator().generate_catalog_graph(catalog)

    assert len(graph) > 5