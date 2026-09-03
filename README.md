# GDI Catalog Builder

git branch -M main
git remote add origin https://github.com/yehiafarag/gdi-catalog-builder.git
git push -u origin main
The project is designed around a simple pipeline:

CSV input
  -> metadata models
  -> RDF graph generation
  -> SHACL validation
  -> Turtle output

It is intended for building catalog metadata that follows the Genomic Data Infrastructure (GDI) metadata patterns and DCAT-style publication conventions.

## What the project does

- Reads semicolon-delimited CSV files
- Maps each row into structured Python models
- Groups rows into a `Catalog` model
- Generates RDF using `rdflib`
- Validates the generated RDF against GDI SHACL shapes
- Writes Turtle output only when validation succeeds

## Core architecture

### Models

The `gdi_catalog_builder.models` package contains the core metadata types used throughout the pipeline:

- `Agent`: a person, organisation, or institutional actor
- `ContactPoint`: a contact email or URL
- `DatasetMetadata`: main dataset metadata record
- `Distribution`: a downloadable or accessible data distribution
- `Identifier`: dataset identifiers and registry references
- `Catalog`: a collection of dataset metadata records

### Converters

The `gdi_catalog_builder.converters` package handles CSV reading and RDF generation:

- `CSVReader`: reads a CSV file and returns row dictionaries
- `CatalogBuilder`: builds a `Catalog` from CSV rows
- `DatasetMapper`: maps a CSV row to `DatasetMetadata`
- `RDFGenerator`: builds an RDF graph for the catalog

### Validators

- `ShaclLoader`: loads all `.ttl` SHACL files from a directory
- `ShaclValidator`: validates RDF data against the loaded SHACL graph

## Repository structure

```text
.can you clean?

├── input/
├── output/
├── schemas/
│   └── gdi/
│       └── PiecesShape/
├── src/
│   └── gdi_catalog_builder/
│       ├── __init__.py
│       ├── cli.py
│       ├── converters/
│       │   ├── catalog_builder.py
│       │   ├── csv_reader.py
│       │   ├── dataset_mapper.py
│       │   └── rdf_generator.py
│       ├── models/
│       │   ├── agent.py
│       │   ├── catalog.py
│       │   ├── contact_point.py
│       │   ├── dataset.py
│       │   ├── distribution.py
│       │   └── identifier.py
│       └── validators/
│           ├── shacl_loader.py
│           └── shacl_validator.py
├── tests/
├── pyproject.toml
├── README.md
└── catalog.ttl
```

## Prerequisites

- Python 3.11 or newer
- `pip`
- Access to the GDI SHACL schema files in `schemas/gdi/PiecesShape`

## Quick start

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the project in editable mode:

```bash
python3 -m pip install --upgrade pip
python3 -m pip install -e .
```

Run the CLI against a CSV source file:

```bash
PYTHONPATH=src python -m gdi_catalog_builder.cli input/your_file.csv
```

The CLI validates the generated RDF and writes the Turtle output into the `output/` directory.

Mode flags:

```bash
PYTHONPATH=src python -m gdi_catalog_builder.cli input/your_file.csv --minimum
PYTHONPATH=src python -m gdi_catalog_builder.cli input/your_file.csv --full
```

- `--minimum`: uses available CSV data and ignores missing values for required fields.
- `--full`: requires required field values to be present (default behavior).

## Example usage

A simple call flow looks like this:

```python
from gdi_catalog_builder.converters.catalog_builder import CatalogBuilder
from gdi_catalog_builder.converters.rdf_generator import RDFGenerator
from gdi_catalog_builder.validators.shacl_loader import ShaclLoader
from gdi_catalog_builder.validators.shacl_validator import ShaclValidator

catalog = CatalogBuilder.from_csv("input/example.csv")
graph = RDFGenerator().generate_catalog_graph(catalog)
shapes = ShaclLoader.load_shapes("schemas/gdi/PiecesShape")
conforms, report = ShaclValidator.validate_graph(graph, shapes)

if conforms:
    graph.serialize("output/example.ttl", format="turtle")
else:
    print(report)
```

## Input format

This project expects semicolon-separated CSV files with columns that map to dataset metadata fields such as:

- `id`
- `name`
- `description`
- `author_name`
- `author_id`
- `publisher_name`
- `publisher_id`
- `contact_point`
- `keywords`
- `theme`
- `access_rights`
- `health_category`
- `external_link`

The exact field set may vary depending on the source CSV, but the mapper is designed around the GDI metadata conventions used by this project.

## Validation

The generated graph is validated against the SHACL shapes stored under `schemas/gdi/PiecesShape`.

If validation fails, the command exits with a non-zero status and prints the SHACL report.

## Testing

Run the project test suite with:

```bash
pytest -q
```

## Documentation notes

The package is already structured around a clear separation of responsibilities:

- models for schema/data representation
- converters for CSV and RDF transformation
- validators for graph-level quality checks

The main documentation improvement still worthwhile for the project is to keep the README aligned with the actual CLI, schema paths, and validation flow as the metadata model evolves. Future improvements could include:

- dedicated API documentation for each model class
- examples of valid CSV files
- sample output Turtle files
- a changelog and versioning policy

## License

This project does not currently declare a license in the repository metadata. If it is intended for public or shared reuse, add an explicit open-source license such as MIT or Apache 2.0.
