from collections.abc import AsyncIterator
from typing import AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.pool import NullPool

from src.api.dependencies import get_tron_service
from src.core import all_settings
from src.DB.models import Base
from src.main import setup_app
from src.services.tron_service import TronService
from tests.mocks import mock_tron_service


@pytest.fixture(scope="session")
def mock_tron_service_fixture() -> TronService:
    return mock_tron_service()


@pytest.fixture(scope="session")
async def async_client(
    mock_tron_service_fixture: TronService,
) -> AsyncGenerator[AsyncClient, None]:
    app = setup_app()
    app.dependency_overrides[get_tron_service] = lambda: mock_tron_service_fixture
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as ac:
        yield ac


@pytest.fixture(scope="session")
async def async_engine() -> AsyncIterator[AsyncEngine]:
    engine = create_async_engine(
        all_settings.database.db_uri, echo=True, future=True, poolclass=NullPool
    )
    yield engine
    await engine.dispose()


@pytest.fixture(scope="session", autouse=True)
async def prepare_database(async_engine: AsyncEngine) -> AsyncIterator[None]:
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield None
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="session")
async def session(async_engine: AsyncEngine) -> AsyncIterator[AsyncSession]:
    async with AsyncSession(async_engine) as session:
        yield session
