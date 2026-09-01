from gdi_catalog_builder.converters.csv_reader import CSVReader
from gdi_catalog_builder.converters.dataset_mapper import DatasetMapper
from gdi_catalog_builder.models.catalog import Catalog


class CatalogBuilder:
    """Build a catalog model from a CSV file in the GDI metadata format."""

    @staticmethod
    def from_csv(file_path: str) -> Catalog:
        rows = CSVReader.read(file_path)

        datasets = [
            DatasetMapper.from_csv_row(row)
            for row in rows
        ]

        return Catalog(
            title="Norwegian GDI Catalog",
            description="GDI datasets provided by the Norwegian node",
            applicable_legislation=[
                "http://data.europa.eu/eli/reg/2025/327/oj"
            ],
            datasets=datasets,
        )