import logging

log = logging.getLogger(__name__)


def prepare_batch(transactions):
    current_index = 0
    batch = dict(transactions=list(), total_value=0)
    latency_leftover = 1000
    while current_index < len(transactions):
        transaction = transactions[current_index]

        if transaction["latency"] > 1000:
            transactions.pop(current_index)
            log.error(f"Invalid transaction {transaction}, skipping")
            continue

        latency = transaction["latency"]
        if latency <= latency_leftover:
            batch["transactions"].append(transactions.pop(current_index))
            batch["total_value"] += transaction["value"]

            latency_leftover -= latency
        else:
            current_index += 1

    batch["time_left"] = latency_leftover
    return batch
