from gdi_catalog_builder.converters.rdf_generator import RDFGenerator
from gdi_catalog_builder.models.catalog import Catalog


def test_catalog_to_rdf():

    catalog = Catalog(
        title="Norwegian GDI Catalog",
        description="Catalog for Norway",
        applicable_legislation=[
            "https://eur-lex.europa.eu/eli/reg/2016/679/oj"
        ],
    )

    graph = RDFGenerator().generate_catalog_graph(catalog)

    assert len(graph) > 0