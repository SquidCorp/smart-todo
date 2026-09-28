from datetime import UTC, datetime
from uuid import uuid4

from smart_todo.db.todos import get_tasks, insert_task, remove_task
from smart_todo.models.todo import StatusEnum, Task, TaskCreate, TaskId


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


def get_all_tasks() -> list[Task]:
    return get_tasks()


def delete_task_by_id(data: TaskId) -> None:
    return remove_task(data.id)
