from datetime import UTC, datetime
from uuid import uuid4

from smart_todo.db.todos import (
    get_task,
    get_tasks,
    insert_task,
    remove_task,
    update_task as persist_task_update,
)
from smart_todo.models.todo import StatusEnum, Task, TaskCreate, TaskId, TaskUpdate


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


def get_task_by_id(id: str) -> Task | None:
    return get_task(id)


def delete_task_by_id(data: TaskId) -> None:
    return remove_task(data.id)


def update_task(data: TaskUpdate) -> Task | None:
    patch = data.model_dump(exclude_unset=True, exclude={"id"})
    if "priority" in patch:
        patch["priority"] = patch["priority"].value
    if "status" in patch:
        patch["status"] = patch["status"].value
    patch["updated_at"] = datetime.now(UTC)
    return persist_task_update(id=data.id, patch=patch)
