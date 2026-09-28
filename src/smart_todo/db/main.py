import warnings
from collections.abc import Iterator
from contextlib import contextmanager
from urllib.parse import urlparse

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, Session
from sqlalchemy.pool import StaticPool

from smart_todo.models.env import env

warnings.filterwarnings("ignore", category=SyntaxWarning, module="turso.lib")


class Base(DeclarativeBase):
    pass


def _https_url(url: str) -> str:
    parsed = urlparse(url)
    if parsed.scheme == "libsql":
        return parsed._replace(scheme="https").geturl()
    return url


def _make_engine() -> Engine:
    if env.TURSO_PERSIST:
        return create_engine(
            "sqlite+turso_sync:///:memory:",
            connect_args={
                "remote_url": _https_url(env.TURSO_DATABASE_URL),
                "auth_token": env.TURSO_AUTH_TOKEN,
            },
            poolclass=StaticPool,
        )
    return create_engine(
        "sqlite+turso:///:memory:",
        poolclass=StaticPool,
    )


engine = _make_engine()


def _push(session: Session) -> None:
    from turso.sqlalchemy import get_sync_connection

    get_sync_connection(session.connection()).push()


@contextmanager
def session_scope() -> Iterator[Session]:
    with Session(engine) as session:
        yield session
        session.commit()
        if env.TURSO_PERSIST:
            _push(session)


def init_db() -> None:
    from smart_todo.db.todos import TaskRow  # noqa: F401

    Base.metadata.create_all(engine)
    if env.TURSO_PERSIST:
        with Session(engine) as session:
            _push(session)
