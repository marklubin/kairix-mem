import uuid
from typing import Optional

from pydantic import BaseModel, Field


class TagBase(BaseModel):
    """Base model for tag operations."""

    name: str = Field(..., min_length=1)


class TagCreate(TagBase):
    """Model for creating a new tag."""

    pass


class TagUpdate(BaseModel):
    """Model for updating an existing tag."""

    name: Optional[str] = None


class Tag(TagBase):
    """Model for a tag."""

    id: uuid.UUID

    model_config = {"from_attributes": True}
