import pytest
import asyncio
from wallet_api.main import app


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def client(aiohttp_client):
    """
    Fixture to test API endpoints.
    :param aiohttp_client:
    :return:
    """
    return await aiohttp_client(app)


@pytest.fixture(autouse=True)
async def patch_manager(mocker):
    async def fake_stop(self):
        tasks = [*self.tasks.values(), self.main_task]
        for t in tasks:
            t.cancel()

    # cancellation without awaiting result, which is not needed for tests
    mocker.patch("wallet_api.background.Background.stop", fake_stop)
