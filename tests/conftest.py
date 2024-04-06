import pytest
import asyncio

from sqlalchemy.ext.asyncio import async_sessionmaker

from wallet_api.main import app
from alchemy.db import get_engine


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def api_client(aiohttp_client):
    """
    Fixture to test API endpoints.
    :param aiohttp_client:
    :return:
    """
    return await aiohttp_client(app)


@pytest.fixture(scope="session")
def engine():
    engine = get_engine()
    yield engine

    engine.dispose()


@pytest.fixture(scope="session")
def session(engine):
    return async_sessionmaker(engine, expire_on_commit=False)


@pytest.fixture(autouse=True)
async def preparations(mocker):
    async def fake_stop(self):
        tasks = self.tasks.values()
        for t in tasks:
            t.cancel()

    # cancellation without awaiting result, which is not needed for tests
    mocker.patch("wallet_api.background.Background.teardown", fake_stop)
