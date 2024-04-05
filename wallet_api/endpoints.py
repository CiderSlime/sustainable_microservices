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

    background.batches += batches
    # potentially heavy operation, consider to use different prioritization or
    # an external batches storage
    background.batches.sort(key=lambda x: x["total_value"])

    return web.Response(status=200)
