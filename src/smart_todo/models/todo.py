from enum import Enum

from pydantic import AwareDatetime, BaseModel, Field


class PriorityEnum(Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class StatusEnum(Enum):
    TODO = "todo"
    DELAYED = "delayed"
    DONE = "done"


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    due: AwareDatetime | None = None
    priority: PriorityEnum = PriorityEnum.MEDIUM


class Task(BaseModel):
    id: str
    title: str = Field(min_length=1, max_length=200)
    due: AwareDatetime
    priority: PriorityEnum
    status: StatusEnum
    created_at: AwareDatetime
    updated_at: AwareDatetime
