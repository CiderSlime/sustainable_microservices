import asyncio
import json

from aiohttp import web
from alchemy.models import Customer
from uuid import UUID
import logging

log = logging.getLogger(__name__)


async def handle_batch(request):
    batch = await request.json()
    session_maker = request.config_dict["session_maker"]

    async with session_maker() as session:
        for transaction in batch["transactions"]:
            customer = await session.get(Customer, UUID(transaction["customer_id"]))
            if not customer:
                transaction["status"] = "customer not found"
            elif customer.balance >= transaction["value"]:
                customer.balance -= transaction["value"]
                await session.commit()
                transaction["status"] = "success"
            else:
                transaction["status"] = "not enough balance"

    return web.json_response(batch["transactions"])
