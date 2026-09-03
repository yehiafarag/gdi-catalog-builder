from pydantic import BaseModel, Field


class Distribution(BaseModel):
    title: str
    access_url: str

    description: dict[str, str] = Field(
        default_factory=dict
    )

    applicable_legislation: list[str] = Field(
        default_factory=list
    )

    format: str | None = None
    media_type: str | None = None
    download_url: str | None = None

    issued: str | None = None
    modified: str | None = None

    rights: dict[str, str] = Field(
        default_factory=dict
    )

    status: str | None = None