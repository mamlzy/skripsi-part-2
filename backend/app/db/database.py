from collections.abc import Generator

from sqlalchemy import create_engine, text
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import get_settings


settings = get_settings()


def _connect_args(database_url: str) -> dict:
    if database_url.startswith("sqlite"):
        return {"check_same_thread": False}
    return {}


source_engine = create_engine(
    settings.source_database_url,
    pool_pre_ping=True,
    future=True,
)

app_engine = create_engine(
    settings.app_database_url,
    connect_args=_connect_args(settings.app_database_url),
    pool_pre_ping=True,
    future=True,
)

SessionLocal = sessionmaker(bind=app_engine, autoflush=False, autocommit=False, future=True)


class Base(DeclarativeBase):
    pass


def get_app_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_app_db() -> None:
    from app.models.dataset import DatasetRisikoPiutang, ModelTrainingRun, PredictionLog

    _ = DatasetRisikoPiutang, ModelTrainingRun, PredictionLog
    Base.metadata.create_all(bind=app_engine)


def check_source_database() -> bool:
    with source_engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    return True


def check_app_database() -> bool:
    with app_engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    return True
