import asyncio


async def test_transactions_endpoint(client):
    sample_transactions = [
        {"value": 110, "latency": 600, "customerId": ""},
        {"value": 70, "latency": 250, "customerId": "" },
        {"value": 200, "latency": 850, "customerId": ""},
        {"value": 120, "latency": 1000, "customerId": ""},
        {"value": 20, "latency": 50, "customerId": ""},
        {"value": 48, "latency": 100, "customerId": ""}
    ]

    resp = await client.post("/transaction", json=sample_transactions)
    assert resp.status == 200

    # wait for mock sending
    await asyncio.sleep(0.1)
    assert not len(client.app["background"].batches)

