import uuid

import pytest
from pydantic import ValidationError

from todo_api.models.tag import Tag, TagCreate, TagUpdate


def test_tag_model() -> None:
    """Test the Tag model with valid input."""
    tag_id = uuid.uuid4()
    tag = Tag(id=tag_id, name="Test Tag")

    assert tag.id == tag_id
    assert tag.name == "Test Tag"


def test_tag_create_model() -> None:
    """Test the TagCreate model with valid input."""
    tag_create = TagCreate(name="New Tag")

    assert tag_create.name == "New Tag"


def test_tag_update_model_empty() -> None:
    """Test the TagUpdate model with no fields set."""
    tag_update = TagUpdate()

    assert tag_update.name is None


def test_tag_update_model_with_name() -> None:
    """Test the TagUpdate model with name set."""
    tag_update = TagUpdate(name="Updated Tag")

    assert tag_update.name == "Updated Tag"


def test_tag_create_validation_error() -> None:
    """Test validation errors for TagCreate model."""
    with pytest.raises(ValidationError):
        TagCreate(name="")
