from collections.abc import AsyncIterator, Callable

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.core.settings import DatabaseSettings


def get_session(
    db_settings: DatabaseSettings,
) -> Callable[[], AsyncIterator[AsyncSession]]:
    async_engine = create_async_engine(
        db_settings.db_uri,
        echo=False,
        pool_size=db_settings.pool_size,
        max_overflow=db_settings.max_overflow,
        connect_args={"timeout": db_settings.timeout},
    )
    async_session_factory = async_sessionmaker(
        bind=async_engine,
        autocommit=False,
        autoflush=False,
        expire_on_commit=False,
    )

    async def recieve_session() -> AsyncIterator[AsyncSession]:
        async with async_session_factory() as session:
            try:
                yield session
                await session.commit()
            except SQLAlchemyError as err:
                await session.rollback()
                raise err

    return recieve_session
