from pathlib import Path

from gdi_catalog_builder.converters.rdf_generator import RDFGenerator
from gdi_catalog_builder.models.catalog import Catalog


def test_ttl_generation():
    catalog = Catalog(
        title="Norwegian GDI Catalog",
        description="Catalog for Norway"
    )

    graph = RDFGenerator().generate_catalog_graph(catalog)

    output_file = Path("catalog.ttl")

    graph.serialize(
        destination=str(output_file),
        format="turtle"
    )

    assert output_file.exists()
