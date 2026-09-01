import csv
from pathlib import Path


class CSVReader:
    """Read semicolon-delimited CSV files into dictionary rows."""

    @staticmethod
    def read(file_path: str) -> list[dict[str, str]]:
        path = Path(file_path)

        with path.open(
                mode="r",
                encoding="utf-8",
                newline="",
        ) as csv_file:
            reader = csv.DictReader(
                csv_file,
                delimiter=";",
            )

            return list(reader)