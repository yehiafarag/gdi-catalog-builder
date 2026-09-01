from gdi_catalog_builder.models.agent import Agent
from gdi_catalog_builder.models.contact_point import ContactPoint
from gdi_catalog_builder.models.dataset import DatasetMetadata


class DatasetMapper:
    """Map a CSV row to the structured dataset metadata model."""

    @staticmethod
    def from_csv_row(row: dict[str, str]) -> DatasetMetadata:
        keywords = DatasetMapper._split_values(row.get("keywords"))
        themes = DatasetMapper._split_values(row.get("theme"))
        applicable_legislation = DatasetMapper._split_values(
            row.get("applicable_legislation")
        )
        health_categories = DatasetMapper._split_values(row.get("health_category"))
        external_links = DatasetMapper._split_values(row.get("external_link"))

        creator = Agent(
            name=row["author_name"].strip(),
            identifier=DatasetMapper._optional_value(row.get("author_id")),
        )

        publisher = Agent(
            name=row["publisher_name"].strip(),
            identifier=DatasetMapper._optional_value(row.get("publisher_id")),
            contact_points=DatasetMapper._create_contact_points(
                row.get("contact_point")
            ),
        )

        return DatasetMetadata(
            identifier=row["id"].strip().upper(),
            title=row["name"].strip(),
            description=DatasetMapper._optional_value(row.get("description")),
            creators=[creator],
            publisher=publisher,
            keyword=keywords,
            theme=themes,
            issued=DatasetMapper._optional_value(row.get("issued")),
            is_referenced_by=external_links,
            access_rights=DatasetMapper._optional_value(row.get("access_rights")),
            applicable_legislation=applicable_legislation,
            health_category=health_categories,
        )

    @staticmethod
    def _create_contact_points(value: str | None) -> list[ContactPoint]:
        contact_points: list[ContactPoint] = []

        for contact_value in DatasetMapper._split_values(value):
            if contact_value.startswith("mailto:"):
                contact_points.append(ContactPoint(email=contact_value))
            else:
                contact_points.append(ContactPoint(url=contact_value))

        return contact_points

    @staticmethod
    def _split_values(value: str | None) -> list[str]:
        if not value:
            return []
        return [item.strip() for item in value.split("|") if item.strip()]

    @staticmethod
    def _optional_value(value: str | None) -> str | None:
        if value is None:
            return None

        cleaned_value = value.strip()
        return cleaned_value or None