import asyncio
import logging
from uuid import uuid4

from aiohttp.web_runner import GracefulExit
from constants import PROCESSOR_MAX_WORKERS, BACKGROUND_TIME_INTERVAL_SECONDS

log = logging.getLogger(__name__)


class Background:
    def __init__(self):
        self.transactions = list()
        self.tasks = dict()

    async def send(self, transaction, transaction_id):
        try:
            # await self._update_replica_delay()
            # send request, write result
            log.debug(f"Sending transaction {transaction}")
            self.transactions.remove(transaction)

        except asyncio.CancelledError:
            # await self.close_pool()
            log.debug(f"Task {transaction_id} successfully cancelled.")
            raise asyncio.CancelledError

        except Exception as e:
            log.exception(e)
            raise GracefulExit()

    async def stop(self):
        tasks = self.tasks.values()
        for t in tasks:
            t.cancel()

        await asyncio.gather(*tasks)

    async def start(self):
        while True:
            try:
                for transaction in self.transactions:
                    transaction_id = uuid4()
                    self.tasks[transaction_id] = asyncio.create_task(
                        self.send(transaction, transaction_id)
                    )

                await asyncio.sleep(BACKGROUND_TIME_INTERVAL_SECONDS)

            except Exception as e:
                log.exception(e)
                raise GracefulExit()
