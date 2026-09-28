from pathlib import Path
from typing import Self

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

_SRC = Path(__file__).resolve().parents[2]
_ROOT = _SRC.parent


class Env(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(_ROOT / ".env", _SRC / ".env"),
        extra="ignore",
    )

    TURSO_PERSIST: bool = False
    TURSO_DATABASE_URL: str = ""
    TURSO_AUTH_TOKEN: str = ""

    @model_validator(mode="after")
    def require_turso_when_persist(self) -> Self:
        if self.TURSO_PERSIST:
            missing = [
                name
                for name, value in (
                    ("TURSO_DATABASE_URL", self.TURSO_DATABASE_URL),
                    ("TURSO_AUTH_TOKEN", self.TURSO_AUTH_TOKEN),
                )
                if not value
            ]
            if missing:
                raise ValueError(
                    "required when TURSO_PERSIST=true: " + ", ".join(missing)
                )
        return self


env = Env()
