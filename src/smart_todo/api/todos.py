from fastapi import APIRouter, status

from smart_todo.models.todo import Task, TaskCreate
from smart_todo.services.todos import create_task

router = APIRouter(prefix="/todos", tags=["todos"])


@router.get("/")
def get_todos() -> list[str]:
    return ["hello", "World"]


@router.post("/", status_code=status.HTTP_201_CREATED)
def post_task(body: TaskCreate) -> Task:
    return create_task(body)
