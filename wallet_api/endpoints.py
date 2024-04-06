import asyncio

from aiohttp import web
from wallet_api.helpers import prepare_batch
import logging

log = logging.getLogger(__name__)


async def handle_transactions(request):
    transactions = await request.json()
    transactions.sort(key=lambda x: x["value"], reverse=True)
    batches = list()
    while transactions:
        batches.append(prepare_batch(transactions))

    for batch in batches:
        logging.debug(f"Prepared transaction: {batch}")

    background = request.config_dict["background"]

    asyncio.ensure_future(background.add_batches(batches))

    return web.Response(status=200)


async def get_customer(request):
    pass
