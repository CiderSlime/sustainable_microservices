# About
`wallet_api` microservice receives transactions list through endpoint, slices
them into chunks, and stores them for another coroutine which sends them to
the `wallet_processor` one by one.
# How to run tests
- `pip install -r requirements.txt`
- `pip install -r requirements_tests.txt`
- `make compose_up` for postgres, microservices and migrations
- `make test` for tests, or use similar Pycharm config
### improvement suggestions
- Consider to use task queue (ex. RabbitMQ) to store chunks, and let the 
`wallet_processor` to read them from the queue.
- Use data validator (Pydantic) to check incoming transactions fields, because
we get them from **external users**

Use ```--log-cli-level=DEBUG``` to show internal logs while running tests.