from fastapi import APIRouter, HTTPException, status

from smart_todo.models.todo import Task, TaskCreate, TaskId, TaskUpdate
from smart_todo.services.todos import (
    create_task,
    delete_task_by_id,
    get_all_tasks,
    get_task_by_id,
    update_task,
)

router = APIRouter(tags=["todos"])


@router.get("/all")
def get_todos() -> list[Task]:
    return get_all_tasks()


@router.get("/{id}")
def get_todo(id: str) -> Task:
    task = get_task_by_id(id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="task not found"
        )
    return task


@router.post("/add", status_code=status.HTTP_201_CREATED)
def post_task(body: TaskCreate) -> Task:
    return create_task(body)


@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(body: TaskId) -> None:
    return delete_task_by_id(body)


@router.patch("/update", status_code=status.HTTP_200_OK)
def patch_task(body: TaskUpdate) -> Task:
    task = update_task(body)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="task not found"
        )
    return task
