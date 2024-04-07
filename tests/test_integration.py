from uuid import UUID

import aiohttp
import asyncio

from sqlalchemy import select, func

from alchemy.models import Customer, Transaction


async def test_integration(customers, session_maker):
    sample_transactions = [
        {"value": 110, "latency": 600, "customer_id": customers[2]},  # Customer Inter, 320 balance
        {"value": 70, "latency": 250, "customer_id": customers[2]},
        {"value": 200, "latency": 850, "customer_id": customers[2]},
        {"value": 120, "latency": 1000, "customer_id": customers[2]},
        {"value": 20, "latency": 50, "customer_id": customers[2]},
        {"value": 48, "latency": 100, "customer_id": customers[2]}
    ]
    async with aiohttp.ClientSession() as aiohttp_session:
        async with aiohttp_session.post("http://0.0.0.0:8080/transaction", json=sample_transactions) as resp:
            assert resp.status == 200

    await asyncio.sleep(0.1)  # some time for communication between api and processor

    async with session_maker() as session:
        # transactions = (await session.execute(select(Transaction))).count()
        count = (await session.execute(select(func.count()).select_from(select(Transaction).subquery()))).scalar_one()
        assert count == 6  # ensure we have stored all transactions results

        customer_inter = await session.get(Customer, UUID(customers[2]))
        assert customer_inter.balance == 52.0  # current algorithm builds first batch with values 200, 48, 20
