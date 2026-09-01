from gdi_catalog_builder.converters.catalog_builder import CatalogBuilder
from gdi_catalog_builder.converters.rdf_generator import RDFGenerator
from gdi_catalog_builder.validators.shacl_loader import ShaclLoader
from gdi_catalog_builder.validators.shacl_validator import ShaclValidator


def test_csv_to_shacl_valid_catalog():
    catalog = CatalogBuilder.from_csv(
        "input/sample_datasets.csv"
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