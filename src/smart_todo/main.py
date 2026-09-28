from contextlib import asynccontextmanager

from fastapi import FastAPI

from smart_todo.api.todos import router as TodoRouter
from smart_todo.db.main import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(TodoRouter, prefix="/tasks")
