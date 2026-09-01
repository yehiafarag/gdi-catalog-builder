from gdi_catalog_builder.converters.rdf_generator import RDFGenerator
from gdi_catalog_builder.models.catalog import Catalog
from gdi_catalog_builder.validators.shacl_loader import ShaclLoader
from gdi_catalog_builder.validators.shacl_validator import ShaclValidator


def test_catalog_shacl_validation():
    catalog = Catalog(
        title="Norwegian GDI Catalog",
        description="Catalog for Norway",
        applicable_legislation=[
            "https://eur-lex.europa.eu/eli/reg/2016/679/oj"
        ],
    )

    data_graph = RDFGenerator().generate_catalog_graph(catalog)

    shapes_graph = ShaclLoader.load_shapes(
        "schemas/gdi/PiecesShape"
    )

    conforms, report = ShaclValidator.validate_graph(
        data_graph=data_graph,
        shapes_graph=shapes_graph,
    )

    print(report)


    assert conforms, report