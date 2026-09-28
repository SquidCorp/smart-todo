from datetime import UTC, datetime

from sqlalchemy import DateTime, String, delete, select
from sqlalchemy.orm import Mapped, mapped_column

from smart_todo.db.main import Base, session_scope
from smart_todo.models.todo import PriorityEnum, StatusEnum, Task


class TaskRow(Base):
    __tablename__ = "tasks"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    due: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    priority: Mapped[str] = mapped_column(String(16), nullable=False)
    status: Mapped[str] = mapped_column(String(16), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )


def _aware(dt: datetime) -> datetime:
    if dt.tzinfo is None:
        return dt.replace(tzinfo=UTC)
    return dt


def _to_task(row: TaskRow) -> Task:
    return Task(
        id=row.id,
        title=row.title,
        due=_aware(row.due),
        priority=PriorityEnum(row.priority),
        status=StatusEnum(row.status),
        created_at=_aware(row.created_at),
        updated_at=_aware(row.updated_at),
    )


def insert_task(
    *,
    id: str,
    title: str,
    due: datetime,
    priority: PriorityEnum,
    status: StatusEnum,
    created_at: datetime,
    updated_at: datetime,
) -> Task:
    row = TaskRow(
        id=id,
        title=title,
        due=due,
        priority=priority.value,
        status=status.value,
        created_at=created_at,
        updated_at=updated_at,
    )
    with session_scope() as session:
        session.add(row)
        session.flush()
        session.refresh(row)
        return _to_task(row)


def get_tasks() -> list[Task]:
    with session_scope() as session:
        rows = session.scalars(
            select(TaskRow).order_by(TaskRow.created_at.desc()).limit(20)
        ).all()
        return [_to_task(row) for row in rows]


def remove_task(id: str) -> None:
    with session_scope() as session:
        session.execute(delete(TaskRow).where(TaskRow.id == id))
