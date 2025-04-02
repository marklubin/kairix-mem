import uuid
from datetime import datetime

import pytest
from pydantic import ValidationError

from todo_api.models.reminder import Reminder, ReminderCreate, ReminderUpdate


def test_reminder_model() -> None:
    """Test the Reminder model with valid input."""
    reminder_id = uuid.uuid4()
    task_id = uuid.uuid4()
    remind_at = datetime.now()

    reminder = Reminder(
        id=reminder_id, task_id=task_id, remind_at=remind_at, completed=False
    )

    assert reminder.id == reminder_id
    assert reminder.task_id == task_id
    assert reminder.remind_at == remind_at
    assert reminder.completed is False


def test_reminder_model_with_defaults() -> None:
    """Test the Reminder model with default values."""
    reminder_id = uuid.uuid4()
    task_id = uuid.uuid4()
    remind_at = datetime.now()

    reminder = Reminder(id=reminder_id, task_id=task_id, remind_at=remind_at)

    assert reminder.id == reminder_id
    assert reminder.task_id == task_id
    assert reminder.remind_at == remind_at
    assert reminder.completed is False


def test_reminder_create_model() -> None:
    """Test the ReminderCreate model with required fields."""
    remind_at = datetime.now()

    reminder_create = ReminderCreate(remind_at=remind_at)

    assert reminder_create.remind_at == remind_at


def test_reminder_update_model_empty() -> None:
    """Test the ReminderUpdate model with no fields set."""
    reminder_update = ReminderUpdate()

    assert reminder_update.remind_at is None
    assert reminder_update.completed is None


def test_reminder_update_model_with_fields() -> None:
    """Test the ReminderUpdate model with fields set."""
    remind_at = datetime.now()

    reminder_update = ReminderUpdate(remind_at=remind_at, completed=True)

    assert reminder_update.remind_at == remind_at
    assert reminder_update.completed is True


def test_reminder_create_validation_error() -> None:
    """Test validation errors for ReminderCreate model."""
    with pytest.raises(ValidationError):
        ReminderCreate()
