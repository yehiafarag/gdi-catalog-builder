from pydantic import BaseModel


class ContactPoint(BaseModel):
    """A contact method associated with a person or organisation."""

    fn: str | None = None
    email: str | None = None
    url: str | None = None
    identifier: str | None = None