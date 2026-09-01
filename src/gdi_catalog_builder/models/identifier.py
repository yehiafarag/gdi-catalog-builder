from typing import Optional

from pydantic import BaseModel


class Identifier(BaseModel):
    """A persistent identifier or registry reference for a dataset."""

    notation: str
    schema_agency: Optional[str] = None
    name: Optional[str] = None