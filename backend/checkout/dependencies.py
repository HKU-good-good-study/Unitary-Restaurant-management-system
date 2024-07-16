from checkout.exceptions import OrderIdRequired, TransactionDataRequired
from checkout.schemas import TransactionCreate


async def valid_order_id(order_id: str) -> str:
    if not order_id:
        raise OrderIdRequired()

    return order_id


async def valid_transaction_data(transaction_data: TransactionCreate) -> TransactionCreate:
    if not transaction_data:
        raise TransactionDataRequired()

    return transaction_data
