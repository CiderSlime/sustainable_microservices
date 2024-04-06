import logging.config

from sqlalchemy.ext.asyncio import async_sessionmaker
from aiohttp import web
from alchemy.db import get_engine
from wallet_processor.handler import handle_batch

log = logging.getLogger(__name__)

engine = get_engine()


async def teardown_app():
    yield
    await engine.dispose()
    log.info("Loop closed. Exiting...")

app = web.Application()
app["session"] = async_sessionmaker(engine, expire_on_commit=False)

app.add_routes([
    web.post("/handler", handle_batch)
])
app.cleanup_ctx.append(teardown_app)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    web.run_app(app, port=8081)
