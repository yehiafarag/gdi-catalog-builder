from pydantic import BaseModel, Field

from gdi_catalog_builder.models.contact_point import ContactPoint


class Agent(BaseModel):
    """Represents a person, organisation, or institutional actor in a dataset."""

    name: str
    identifier: str | None = None
    contact_points: list[ContactPoint] = Field(default_factory=list)