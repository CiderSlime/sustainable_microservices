from uuid import UUID

from alchemy.models import Customer


async def test_transactions_endpoint(api_client, customers, mocker):
    async def send_batch_mock(self, batch):
        await self.handle_next_batch()

    # cross-ms logic, should keep it for integration test
    mocker.patch("wallet_api.background.Background.send_batch", send_batch_mock)

    sample_transactions = [
        {"value": 110, "latency": 600, "customer_id": customers[0]},
        {"value": 70, "latency": 250, "customer_id": customers[1]},
    ]

    resp = await api_client.post("/transaction", json=sample_transactions)
    assert resp.status == 200


async def test_processor_handler_endpoint(processor_client, customers, session_maker):
    sample_batch = {
        'transactions': [
            {'value': 200, 'latency': 850, 'customer_id': customers[1]},    # Smith, balance 800
            {'value': 48, 'latency': 100, 'customer_id': customers[1]},
            {'value': 20, 'latency': 50, 'customer_id': customers[0]},      # John, balance 700
            {'value': 2000, 'latency': 0, 'customer_id': customers[0]}
        ], 'total_value': 268, 'time_left': 0}

    resp = await processor_client.post("/handler", json=sample_batch)
    assert resp.status == 200

    async with session_maker() as session:
        customer_smith = await session.get(Customer, UUID(customers[1]))
        assert customer_smith.balance == 552.0

        customer_john = await session.get(Customer, UUID(customers[0]))
        assert customer_john.balance == 680.0


