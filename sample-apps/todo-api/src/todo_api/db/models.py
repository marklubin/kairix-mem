from datetime import date, datetime
import uuid
from typing import List, Optional

from sqlalchemy import Boolean, Column, Date, DateTime, ForeignKey, String, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column, relationship

Base = declarative_base()


# Association table for the many-to-many relationship between Task and Tag
task_tag = Table(
    "task_tag",
    Base.metadata,
    Column("task_id", UUID(as_uuid=True), ForeignKey("tasks.id"), primary_key=True),
    Column("tag_id", UUID(as_uuid=True), ForeignKey("tags.id"), primary_key=True),
)


class Task(Base):
    """SQLAlchemy model for a task."""

    __tablename__ = "tasks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    completed = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    due_date = Column(Date, nullable=True)
    additional_details = Column(String, nullable=True)

    # Relationships
    tags: Mapped[List["Tag"]] = relationship(
        "Tag", secondary=task_tag, back_populates="tasks"
    )
    reminders: Mapped[List["Reminder"]] = relationship(
        "Reminder", back_populates="task", cascade="all, delete-orphan"
    )


class Tag(Base):
    """SQLAlchemy model for a tag."""

    __tablename__ = "tags"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False, unique=True)

    # Relationships
    tasks: Mapped[List["Task"]] = relationship(
        "Task", secondary=task_tag, back_populates="tags"
    )


class Reminder(Base):
    """SQLAlchemy model for a reminder."""

    __tablename__ = "reminders"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    task_id = Column(
        UUID(as_uuid=True), ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False
    )
    remind_at = Column(DateTime, nullable=False)
    completed = Column(Boolean, default=False, nullable=False)

    # Relationships
    task: Mapped["Task"] = relationship("Task", back_populates="reminders")


class APIKey(Base):
    """SQLAlchemy model for an API key."""

    __tablename__ = "api_keys"

    key = Column(String, primary_key=True)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)