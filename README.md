# Wallet_api
`wallet_api` microservice receives transactions list through endpoint, slices
them into chunks, and stores them for another coroutine which sends them to
the `wallet_processor` one by one.
### improvement suggestions
- Consider to use task queue (ex. RabbitMQ) to store chunks, and let the 
`wallet_processor` to read them from the queue.
- Use data validator (Pydantic) to check incoming transactions fields, because
we get them from **external users**

Use ```--log-cli-level=DEBUG``` to show internal logs while running tests.