import asyncio

from aiohttp import web
from alchemy.models import Customer
import logging

log = logging.getLogger(__name__)


async def handle_batch(request):
    batch = await request.json()
    session = request.config_dict["session"]
    for transaction in batch["transactions"]:
        async with session() as session:
            customer = await session.get(Customer, transaction["customerId"])
            if customer.balance >= transaction["value"]:
                customer.balance -= transaction["value"]
                await session.commit()
                transaction["status"] = "success"
            else:
                transaction["status"] = "not enough balance"
    return web.json_response(batch["transactions"])
