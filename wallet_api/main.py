import logging.config

from aiohttp import web
from wallet_api.background import Background
from wallet_api.endpoints import handle_transactions

log = logging.getLogger(__name__)


async def background_task(app):
    """
    This func yields twice, first time when running app,
    second time on shutdown. Cancels update_state before shutdown.
    """
    app["background"].start()
    log.info("Background task started.")
    yield
    await app["background"].stop()

    log.info("Loop closed. Exiting...")

app = web.Application()
app["background"] = Background()

app.add_routes([
    web.post("/transaction", handle_transactions),
    # web.get("/is_ready", views.readiness_probe),
    # web.get("/{dns}", views.get_fastest_replica_per_dns),
])
app.cleanup_ctx.append(background_task)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    web.run_app(app)
