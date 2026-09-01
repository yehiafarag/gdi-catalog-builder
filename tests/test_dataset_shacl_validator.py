from gdi_catalog_builder.converters.rdf_generator import RDFGenerator
from gdi_catalog_builder.models.catalog import Catalog
from gdi_catalog_builder.models.dataset import DatasetMetadata
from gdi_catalog_builder.validators.shacl_loader import ShaclLoader
from gdi_catalog_builder.validators.shacl_validator import ShaclValidator
from gdi_catalog_builder.models.agent import Agent


def test_valid_dataset_shacl_validation():
    catalog = Catalog(
        title="Norwegian GDI Catalog",
        description="Catalog for Norway",
        applicable_legislation=[
            "https://eur-lex.europa.eu/eli/reg/2016/679/oj"
        ],
        datasets=[
            DatasetMetadata(
                title="Norwegian Cancer Dataset",
                description="A test dataset for GDI validation",
                identifier="GDI-NO-UIO-001",
                access_rights=(
                    "http://publications.europa.eu/"
                    "resource/authority/access-right/RESTRICTED"
                ),
                applicable_legislation=[
                    "http://data.europa.eu/eli/reg/2025/327/oj"
                ],
                creators=[
                    Agent(name="University of Oslo")
                ],
                publisher=Agent(name="ELIXIR Norway"),
                health_category=[
                    "http://data.gdi.eu/core/p2/HealthCategoryHumanGenomic"
                ],
                theme=[
                    "http://publications.europa.eu/resource/authority/data-theme/HEAL"
                ],

            )
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