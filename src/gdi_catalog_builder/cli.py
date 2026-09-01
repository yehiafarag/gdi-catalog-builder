import argparse
from pathlib import Path

from gdi_catalog_builder.converters.catalog_builder import CatalogBuilder
from gdi_catalog_builder.converters.rdf_generator import RDFGenerator
from gdi_catalog_builder.validators.shacl_loader import ShaclLoader
from gdi_catalog_builder.validators.shacl_validator import ShaclValidator


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert GDI dataset metadata from CSV to Turtle."
    )

    parser.add_argument(
        "input",
        type=Path,
        help="Path to the semicolon-separated CSV input file.",
    )

    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path("catalog.ttl"),
        help="Path for the generated Turtle file. Default: catalog.ttl",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_arguments()

    input_file = args.input
    output_directory = Path("output")
    output_directory.mkdir(parents=True, exist_ok=True)
    output_file = output_directory / input_file.with_suffix(".ttl").name
    shapes_directory = Path("schemas/gdi/PiecesShape")

    if not input_file.is_file():
        print(f"Input file does not exist: {input_file}")
        raise SystemExit(1)

    catalog = CatalogBuilder.from_csv(str(input_file))
    data_graph = RDFGenerator().generate_catalog_graph(catalog)

    shapes_graph = ShaclLoader.load_shapes(
        str(shapes_directory)
    )

    conforms, report = ShaclValidator.validate_graph(
        data_graph=data_graph,
        shapes_graph=shapes_graph,
    )

    if not conforms:
        print("GDI SHACL validation failed:")
        print(report)
        raise SystemExit(1)

    data_graph.serialize(
        destination=str(output_file),
        format="turtle",
    )

    print("GDI SHACL validation passed.")
    print(f"Created: {output_file}")


if __name__ == "__main__":
    main()