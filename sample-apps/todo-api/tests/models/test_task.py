from datetime import date, datetime
import uuid
from typing import List, Optional

import pytest
from pydantic import ValidationError

from todo_api.models.task import Task, TaskCreate, TaskUpdate


def test_task_model() -> None:
    """Test the Task model with valid input."""
    task_id = uuid.uuid4()
    created_at = datetime.now()
    task = Task(
        id=task_id,
        title="Test Task",
        completed=False,
        created_at=created_at,
        tags=[],
        reminders=[]
    )
    
    assert task.id == task_id
    assert task.title == "Test Task"
    assert task.completed is False
    assert task.created_at == created_at
    assert task.due_date is None
    assert task.additional_details is None
    assert task.tags == []
    assert task.reminders == []


def test_task_model_with_optional_fields() -> None:
    """Test the Task model with all fields, including optional ones."""
    task_id = uuid.uuid4()
    created_at = datetime.now()
    due_date = date.today()
    
    task = Task(
        id=task_id,
        title="Test Task with Optional Fields",
        completed=True,
        created_at=created_at,
        due_date=due_date,
        additional_details="These are additional details",
        tags=[],
        reminders=[]
    )
    
    assert task.id == task_id
    assert task.title == "Test Task with Optional Fields"
    assert task.completed is True
    assert task.created_at == created_at
    assert task.due_date == due_date
    assert task.additional_details == "These are additional details"
    assert task.tags == []
    assert task.reminders == []


def test_task_create_model() -> None:
    """Test the TaskCreate model with minimal fields."""
    task_create = TaskCreate(title="New Task")
    
    assert task_create.title == "New Task"
    assert task_create.completed is False
    assert task_create.due_date is None
    assert task_create.additional_details is None
    assert task_create.tag_ids == []


def test_task_create_model_with_all_fields() -> None:
    """Test the TaskCreate model with all fields."""
    tag_ids = [uuid.uuid4(), uuid.uuid4()]
    due_date = date.today()
    
    task_create = TaskCreate(
        title="New Task with All Fields",
        completed=True,
        due_date=due_date,
        additional_details="Additional info",
        tag_ids=tag_ids
    )
    
    assert task_create.title == "New Task with All Fields"
    assert task_create.completed is True
    assert task_create.due_date == due_date
    assert task_create.additional_details == "Additional info"
    assert task_create.tag_ids == tag_ids


def test_task_update_model() -> None:
    """Test the TaskUpdate model with no fields set."""
    task_update = TaskUpdate()
    
    assert task_update.title is None
    assert task_update.completed is None
    assert task_update.due_date is None
    assert task_update.additional_details is None
    assert task_update.tag_ids is None


def test_task_update_model_with_fields() -> None:
    """Test the TaskUpdate model with fields set."""
    tag_ids = [uuid.uuid4(), uuid.uuid4()]
    due_date = date.today()
    
    task_update = TaskUpdate(
        title="Updated Task",
        completed=True,
        due_date=due_date,
        additional_details="Updated details",
        tag_ids=tag_ids
    )
    
    assert task_update.title == "Updated Task"
    assert task_update.completed is True
    assert task_update.due_date == due_date
    assert task_update.additional_details == "Updated details"
    assert task_update.tag_ids == tag_ids


def test_task_create_validation_error() -> None:
    """Test validation errors for TaskCreate model."""
    with pytest.raises(ValidationError):
        TaskCreate(title="")  # Empty title should fail