from pydantic import BaseModel, Field

from gdi_catalog_builder.models.agent import Agent
from gdi_catalog_builder.models.distribution import Distribution
from gdi_catalog_builder.models.identifier import Identifier


class DatasetMetadata(BaseModel):
    """Metadata describing a dataset in the GDI catalog."""

    title: str
    description: str | None = None
    identifier: str | None = None

    creators: list[Agent] = Field(default_factory=list)
    publisher: Agent | None = None
    distributions: list[Distribution] = Field(default_factory=list)
    identifiers: list[Identifier] = Field(default_factory=list)

    access_rights: str | None = None
    applicable_legislation: list[str] = Field(default_factory=list)

    status: str | None = None
    theme: list[str] = Field(default_factory=list)
    keyword: list[str] = Field(default_factory=list)
    health_category: list[str] = Field(default_factory=list)
    type: str | None = None

    conforms_to: list[str] = Field(default_factory=list)
    legal_basis: list[str] = Field(default_factory=list)

    number_of_records: int | None = None
    number_of_unique_individuals: int | None = None

    is_referenced_by: list[str] = Field(default_factory=list)
    issued: str | None = None