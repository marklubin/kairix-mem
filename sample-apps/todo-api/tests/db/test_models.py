import uuid
from datetime import date, datetime

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from todo_api.db.models import Base, Task, Tag, Reminder
from todo_api.db.session import get_db


# Use in-memory SQLite for testing
DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture
async def db_engine():
    """Create an async SQLite engine for testing."""
    engine = create_async_engine(DATABASE_URL, echo=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest.fixture
async def db_session(db_engine):
    """Create a test database session."""
    async_session = sessionmaker(
        db_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session


@pytest.mark.asyncio
async def test_create_task(db_session):
    """Test creating a task in the database."""
    task = Task(
        id=uuid.uuid4(),
        title="Test Task",
        completed=False,
        created_at=datetime.now(),
        due_date=None,
        additional_details=None,
    )
    db_session.add(task)
    await db_session.commit()
    await db_session.refresh(task)

    assert task.id is not None
    assert task.title == "Test Task"
    assert task.completed is False
    assert task.created_at is not None
    assert task.tags == []
    assert task.reminders == []


@pytest.mark.asyncio
async def test_create_tag(db_session):
    """Test creating a tag in the database."""
    tag = Tag(id=uuid.uuid4(), name="Test Tag")
    db_session.add(tag)
    await db_session.commit()
    await db_session.refresh(tag)

    assert tag.id is not None
    assert tag.name == "Test Tag"
    assert tag.tasks == []


@pytest.mark.asyncio
async def test_create_reminder(db_session):
    """Test creating a reminder in the database."""
    task = Task(
        id=uuid.uuid4(),
        title="Test Task with Reminder",
        completed=False,
        created_at=datetime.now(),
    )
    db_session.add(task)
    await db_session.commit()

    reminder = Reminder(
        id=uuid.uuid4(),
        task_id=task.id,
        remind_at=datetime.now(),
        completed=False,
    )
    db_session.add(reminder)
    await db_session.commit()
    await db_session.refresh(reminder)
    await db_session.refresh(task)

    assert reminder.id is not None
    assert reminder.task_id == task.id
    assert reminder.remind_at is not None
    assert reminder.completed is False
    assert len(task.reminders) == 1
    assert task.reminders[0].id == reminder.id


@pytest.mark.asyncio
async def test_task_with_tags(db_session):
    """Test associating tags with a task."""
    task = Task(
        id=uuid.uuid4(),
        title="Task with Tags",
        completed=False,
        created_at=datetime.now(),
    )
    tag1 = Tag(id=uuid.uuid4(), name="Tag 1")
    tag2 = Tag(id=uuid.uuid4(), name="Tag 2")

    db_session.add_all([task, tag1, tag2])
    await db_session.commit()

    task.tags.append(tag1)
    task.tags.append(tag2)
    await db_session.commit()
    await db_session.refresh(task)

    assert len(task.tags) == 2
    assert task.tags[0].name == "Tag 1"
    assert task.tags[1].name == "Tag 2"

    await db_session.refresh(tag1)
    assert len(tag1.tasks) == 1
    assert tag1.tasks[0].id == task.id