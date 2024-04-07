import logging.config
import pathlib
import sys

directory = pathlib.Path(__file__).parent.parent.absolute()
sys.path.append(str(directory))

from sqlalchemy.ext.asyncio import async_sessionmaker
from aiohttp import web
from wallet_api.background import Background
from wallet_api.endpoints import handle_transactions
from alchemy.db import get_engine

log = logging.getLogger(__name__)

engine = get_engine()


async def teardown_app(app):
    yield
    await app["background"].teardown()
    await engine.dispose()
    log.info("Loop closed. Exiting...")

app = web.Application()
app["background"] = Background(async_sessionmaker(engine, expire_on_commit=False))

app.add_routes([
    web.post("/transaction", handle_transactions),
    # web.get("/is_ready", views.readiness_probe),
    # web.get("/{dns}", views.get_fastest_replica_per_dns),
])
app.cleanup_ctx.append(teardown_app)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    web.run_app(app)
