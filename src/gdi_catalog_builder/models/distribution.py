from typing import Optional

from pydantic import BaseModel, Field


class Distribution(BaseModel):
    """A downloadable or accessible distribution of a dataset."""

    title: str
    access_url: str
    applicable_legislation: list[str] = Field(default_factory=list)
    status: Optional[str] = None