from fastapi import APIRouter, status

from smart_todo.models.todo import Task, TaskCreate, TaskId
from smart_todo.services.todos import create_task, delete_task_by_id, get_all_tasks

router = APIRouter(tags=["todos"])


@router.get("/all")
def get_todos() -> list[Task]:
    return get_all_tasks()


@router.post("/add", status_code=status.HTTP_201_CREATED)
def post_task(body: TaskCreate) -> Task:
    return create_task(body)


@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(body: TaskId) -> None:
    return delete_task_by_id(body)
