import pytest
import asyncio
import uuid

from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy import select

from alchemy.models import Customer, Transaction
from wallet_api.main import app as api_app
from wallet_processor.main import app as processor_app
from alchemy.db import get_engine


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def api_client(aiohttp_client):
    """
    Fixture to test API endpoints for Wallet_Api.
    """
    return await aiohttp_client(api_app)


@pytest.fixture
async def processor_client(aiohttp_client):
    """
    Fixture to test API endpoints for Wallet_Processor.
    """
    return await aiohttp_client(processor_app)


@pytest.fixture(scope="session")
def engine():
    engine = get_engine()
    return engine


@pytest.fixture(scope="session")
def session_maker(engine):
    return async_sessionmaker(engine, expire_on_commit=False)


@pytest.fixture(scope="session")
async def customers(session_maker):
    customers_id = [str(uuid.uuid4()) for _ in range(3)]
    async with session_maker() as session:

        transactions = (await session.execute(select(Transaction))).scalars().all()
        for transaction in transactions:
            await session.delete(transaction)

        customers = (await session.execute(select(Customer))).scalars().all()
        for customer in customers:
            await session.delete(customer)

        await session.commit()

        async with session.begin():
            session.add_all([
                Customer(
                    uid=customers_id[0],
                    username='John', password="123",
                    balance=700.0
                ),
                Customer(
                    uid=customers_id[1],
                    username='Smith', password="321",
                    balance=800.0
                ),
                Customer(
                    uid=customers_id[2],
                    username='Inter', password="777",
                    balance=320.0
                ),
            ])
            return customers_id
