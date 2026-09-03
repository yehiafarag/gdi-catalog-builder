from gdi_catalog_builder.models.agent import Agent
from gdi_catalog_builder.models.contact_point import ContactPoint
from gdi_catalog_builder.models.dataset import DatasetMetadata
from gdi_catalog_builder.models.distribution import Distribution


class DatasetMapper:
    """Map a CSV row to the structured dataset metadata model."""

    @staticmethod
    def from_csv_row(
        row: dict[str, str],
        *,
        strict_required: bool = True,
    ) -> DatasetMetadata:
        keywords = DatasetMapper._split_values(
            row.get("keywords"),
            separators=(",", "|"),
        )
        themes = DatasetMapper._split_values(row.get("theme"))
        applicable_legislation = DatasetMapper._split_values(
            row.get("applicable_legislation")
        )
        if not applicable_legislation:
            applicable_legislation = [
                "http://data.europa.eu/eli/reg/2025/327/oj"
            ]
        health_categories = DatasetMapper._split_values(row.get("health_category"))

        dataset_identifier = DatasetMapper._required_or_optional(
            row.get("id"),
            "id",
            strict_required,
        )
        dataset_title = DatasetMapper._required_or_optional(
            row.get("name"),
            "name",
            strict_required,
        )

        creator_name = DatasetMapper._required_or_optional(
            row.get("author_name"),
            "author_name",
            strict_required,
        )
        creator = Agent(
            name=creator_name or "Unknown author",
            identifier=DatasetMapper._optional_value(row.get("author_id")),
        )

        publisher_name = DatasetMapper._required_or_optional(
            row.get("publisher_name"),
            "publisher_name",
            strict_required,
        )

        publisher_contact_points = DatasetMapper._create_contact_points(
            row.get("contact_point")
        )
        publisher = None
        if publisher_name:
            publisher = Agent(
                name=publisher_name,
                identifier=DatasetMapper._optional_value(row.get("publisher_id")),
                contact_points=publisher_contact_points,
            )

        distribution_access_url = DatasetMapper._optional_value(row.get("external_link"))
        distributions: list[Distribution] = []
        if distribution_access_url:
            distributions.append(
                Distribution(
                    title=(
                        f"Distribution for {dataset_title or 'Untitled dataset'}"
                    ),
                    description={
                        "en": (
                            "Distribution providing access to the "
                            f"{dataset_title or 'Untitled dataset'}"
                        )
                    },
                    access_url=distribution_access_url,
                    download_url=distribution_access_url,
                    applicable_legislation=applicable_legislation,
                    format="HTML",
                    media_type="text/html",
                    issued=DatasetMapper._optional_value(row.get("issued")),
                    rights={"en": " "},
                )
            )

        publisher_email = None
        if publisher_contact_points:
            first_contact = publisher_contact_points[0]
            publisher_email = first_contact.email

        dataset_contact_points = []
        if creator_name and publisher_email:
            dataset_contact_points.append(
                ContactPoint(
                    fn=DatasetMapper._optional_value(creator_name),
                    email=DatasetMapper._normalize_email(publisher_email),
                    identifier=DatasetMapper._optional_value(row.get("author_id")),
                )
            )

        return DatasetMetadata(
            identifier=(dataset_identifier.upper() if dataset_identifier else None),
            title=dataset_title or "Untitled dataset",
            description=DatasetMapper._optional_value(row.get("description")),
            creators=[creator],
            publisher=publisher,
            keyword=keywords,
            theme=themes,
            issued=DatasetMapper._optional_value(row.get("issued")),
            access_rights=DatasetMapper._optional_value(row.get("access_rights")),
            applicable_legislation=applicable_legislation,
            health_category=health_categories,
            distributions=distributions,
            contact_points=dataset_contact_points,
            provenance={"en": "Created and maintained by the University of Bergen."},
            type=(
                "https://publications.europa.eu/resource/authority/dataset-type/"
                "SYNTHETIC_DATA"
            ),
            version_notes={
                "en": "Initial metadata version for the Norwegian GDI catalog."
            },
            is_referenced_by=[distribution_access_url] if distribution_access_url else [],
        )

    @staticmethod
    def _create_contact_points(value: str | None) -> list[ContactPoint]:
        contact_points: list[ContactPoint] = []

        for contact_value in DatasetMapper._split_values(value):
            normalized = contact_value.strip()
            if normalized.startswith("mailto:"):
                contact_points.append(ContactPoint(email=normalized))
            elif "@" in normalized and not normalized.startswith(("http://", "https://")):
                contact_points.append(ContactPoint(email=f"mailto:{normalized}"))
            else:
                contact_points.append(ContactPoint(url=normalized))

        return contact_points

    @staticmethod
    def _normalize_email(value: str | None) -> str | None:
        if not value:
            return None

        normalized = value.strip()
        if normalized.startswith("mailto:"):
            return normalized
        if "@" in normalized and not normalized.startswith(("http://", "https://")):
            return f"mailto:{normalized}"
        return None

    @staticmethod
    def _split_values(
        value: str | None,
        *,
        separators: tuple[str, ...] = ("|",),
    ) -> list[str]:
        if not value:
            return []

        normalized_value = value
        for separator in separators[1:]:
            normalized_value = normalized_value.replace(separator, separators[0])

        return [
            item.strip()
            for item in normalized_value.split(separators[0])
            if item.strip()
        ]

    @staticmethod
    def _optional_value(value: str | None) -> str | None:
        if value is None:
            return None

        cleaned_value = value.strip()
        return cleaned_value or None

    @staticmethod
    def _required_or_optional(
        value: str | None,
        field_name: str,
        strict_required: bool,
    ) -> str | None:
        cleaned_value = DatasetMapper._optional_value(value)
        if cleaned_value is not None:
            return cleaned_value

        if strict_required:
            raise ValueError(f"Missing required CSV column value: {field_name}")

        return None