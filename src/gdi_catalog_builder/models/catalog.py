from typing import Optional

from pydantic import BaseModel, Field

from gdi_catalog_builder.models.dataset import DatasetMetadata


class Catalog(BaseModel):
    """A collection of dataset metadata records for publication as a catalog."""

    title: str
    description: Optional[str] = None
    # A list of applicable legislation
    applicable_legislation: list[str] = Field(default_factory=list)
    datasets: list[DatasetMetadata] = Field(default_factory=list)