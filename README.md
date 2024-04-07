# About
`wallet_api` microservice receives transactions list through endpoint, slices
them into chunks, and stores them for another coroutine which sends them to
the `wallet_processor` one by one.
# How to run tests
- `pip install -r requirements.txt`
- `pip install -r requirements_tests.txt`
- `docker-compose up -d` for postgres
- `alembic upgrade head`
- `python wallet_api/main.py`, then `python wallet_processor/main.py` or use Pycharm run configuration. Required for integration test.
- `pytest tests --log-cli-level=DEBUG` for tests, or use similar Pycharm config
### improvement suggestions
- Consider to use task queue (ex. RabbitMQ) to store chunks, and let the 
`wallet_processor` to read them from the queue.
- Use data validator (Pydantic) to check incoming transactions fields, because
we get them from **external users**

Use ```--log-cli-level=DEBUG``` to show internal logs while running tests.