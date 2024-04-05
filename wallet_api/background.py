import asyncio
import logging
from uuid import uuid4

from aiohttp.web_runner import GracefulExit
from wallet_api.constants import (
    PROCESSOR_MAX_WORKERS,
    BACKGROUND_TIME_INTERVAL_SECONDS
)

log = logging.getLogger(__name__)


class Background:
    def __init__(self):
        self.batches = list()
        self.tasks = dict()
        self.main_task = None

    async def send_transactions(
        self,
        # transaction, transaction_id
    ):
        while True:
            try:
                while self.batches:
                    # transaction_id = uuid4()
                    # send request, write result
                    batch = self.batches.pop()
                    log.debug(f"Sending batch {batch}")
                    # self.tasks[transaction_id] = asyncio.create_task(
                    #     self.send(transaction, transaction_id)
                    # )

                await asyncio.sleep(BACKGROUND_TIME_INTERVAL_SECONDS)

            except asyncio.CancelledError:
                # await self.close_pool()
                log.debug(f"Main task successfully cancelled.")
                raise asyncio.CancelledError

            except Exception as e:
                log.exception(e)
                raise GracefulExit()

    async def stop(self):
        tasks = [self.main_task, *self.tasks.values()]
        for t in tasks:
            t.cancel()

        await asyncio.gather(*tasks)

    def start(self):
        try:
            self.main_task = asyncio.create_task(self.send_transactions())

        except Exception as e:
            log.exception(e)
            raise GracefulExit()
