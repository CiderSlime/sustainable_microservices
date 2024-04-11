import asyncio
import json
import logging
from uuid import uuid4

import aiohttp

from alchemy.models import Transaction
from wallet_api.constants import (
    PROCESSOR_MAX_WORKERS,
)

log = logging.getLogger(__name__)


class Background:
    def __init__(self, session_maker):
        self.session_maker = session_maker
        self.batches = list()
        self.transferring_batches_count = 0

    async def add_batches(self, new_batches):
        self.batches = sorted(self.batches + new_batches, key=lambda x: x["total_value"])
        await self.handle_next_batch()

    async def handle_next_batch(self):
        if self.transferring_batches_count < PROCESSOR_MAX_WORKERS and len(self.batches):
            await self.send_batch(self.batches.pop())

    async def send_batch(self, batch):
        self.transferring_batches_count += 1
        log.debug(f"Sending batch {batch}")
        async with aiohttp.ClientSession() as aiohttp_session:
            async with aiohttp_session.post("http://0.0.0.0:8081/handler", json=batch) as resp:
                transactions = await resp.json(content_type=resp.content_type)
                log.debug(f"Response data: {transactions}")

                async with self.session_maker() as session:
                    async with session.begin():
                        session.add_all([
                            Transaction(
                                uid=str(uuid4()),
                                value=transaction["value"],
                                latency=transaction["latency"],
                                customer_id=transaction["customer_id"],
                                status=transaction["status"],
                            ) for transaction in transactions
                        ])

        self.transferring_batches_count -= 1
        await self.handle_next_batch()
