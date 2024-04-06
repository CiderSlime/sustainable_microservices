import asyncio


async def test_transactions_endpoint(api_client):
    sample_transactions = [
        {"value": 110, "latency": 600, "customerId": 1},
        {"value": 70, "latency": 250, "customerId": 2},
        {"value": 200, "latency": 850, "customerId": 2},
        {"value": 120, "latency": 1000, "customerId": 1},
        {"value": 20, "latency": 50, "customerId": 1},
        {"value": 48, "latency": 100, "customerId": 2}
    ]

    resp = await api_client.post("/transaction", json=sample_transactions)
    assert resp.status == 200

    # wait for mock sending
    await asyncio.sleep(0.1)
    assert not len(api_client.app["background"].batches)

