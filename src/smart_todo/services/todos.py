from datetime import UTC, datetime
from uuid import uuid4

from smart_todo.db.todos import insert_task
from smart_todo.models.todo import StatusEnum, Task, TaskCreate


def create_task(data: TaskCreate) -> Task:
    now = datetime.now(UTC)
    return insert_task(
        id=str(uuid4()),
        title=data.title,
        due=data.due or now,
        priority=data.priority,
        status=StatusEnum.TODO,
        created_at=now,
        updated_at=now,
    )
