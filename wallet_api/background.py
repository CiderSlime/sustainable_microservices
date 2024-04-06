import asyncio
import logging
from uuid import uuid4

from aiohttp.web_runner import GracefulExit
from wallet_api.constants import (
    PROCESSOR_MAX_WORKERS,
)

log = logging.getLogger(__name__)


class Background:
    def __init__(self):
        self.batches = list()
        self.tasks = dict()
        self.main_task = None
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
        self.transferring_batches_count -= 1
        await self.handle_next_batch()

    async def teardown(self):
        tasks = self.tasks.values()
        for t in tasks:
            t.cancel()

        await asyncio.gather(*tasks)
