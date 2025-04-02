from datetime import datetime
import uuid
from typing import Optional

from pydantic import BaseModel


class ReminderBase(BaseModel):
    """Base model for reminder operations."""
    remind_at: datetime


class ReminderCreate(ReminderBase):
    """Model for creating a new reminder."""
    pass


class ReminderUpdate(BaseModel):
    """Model for updating an existing reminder."""
    remind_at: Optional[datetime] = None
    completed: Optional[bool] = None


class Reminder(ReminderBase):
    """Model for a reminder."""
    id: uuid.UUID
    task_id: uuid.UUID
    completed: bool = False
    
    model_config = {"from_attributes": True}