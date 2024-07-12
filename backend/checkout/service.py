from typing import Any, List, Dict

import stripe.checkout
from bson import ObjectId
from fastapi import Depends
from config import app_config
from checkout.config import checkout_config

from checkout.exceptions import TransactionAlreadyExists, StripeError, TransactionAlreadySuccessful
from checkout.schemas import Transaction, TransactionCreate, TransactionStatus
from database import Database
from menu.models import Menu
from table.schemas import Order

db = Database()  # Create an instance of the Database class


async def get_order_by_id(order_id: str) -> Order | None:
    return await db.fetch_one("orders", {"id": order_id})


async def get_transaction_by_order_id(order_id: str) -> Transaction | None:
    return await db.fetch_one("transaction", {"order_id": order_id})


async def get_price_by_dish_name(dish_name: str) -> float:
    dish = await db.fetch_one("menus", {"name": dish_name})
    return float(dish["price"])


async def get_amount_by_order_id(order_id: str) -> float:
    order = await get_order_by_id(order_id)
    dishes = order["dish"]

    total = 0
    for dish in dishes:
        price = await get_price_by_dish_name(dish)
        total += price * dishes[dish]["amount"]

    return total


async def get_line_items_by_order_id(order_id: str) -> list[dict[str, Any]]:
    order = await get_order_by_id(order_id)
    dishes = order["dish"]

    line_items = []
    for dish in dishes:
        price = await get_price_by_dish_name(dish)
        line_items.append(
            {
                "price_data": {
                    "currency": "hkd",
                    "product_data": {"name": dish},
                    "unit_amount_decimal": f"{float(price * 100):.2f}",
                },
                "quantity": dishes[dish]["amount"],
            }
        )

    return line_items


async def save_transaction(transaction: Transaction) -> dict[str, Any]:
    transaction_data = {
        "created_at": transaction.created_at,
        "order_id": transaction.order_id,
        "user_id": transaction.user_id,
        "stripe_session_id": transaction.stripe_session_id,
        "status": transaction.status.value,
        "amount": transaction.amount
    }
    return await db.execute("transaction", transaction_data, "insert")


async def get_transaction_by_session_id(session_id: str) -> Transaction | None:
    return await db.fetch_one("transaction", {"stripe_session_id": session_id})


async def get_transaction_by_user_id(user_id: str) -> list[dict[str, Any]]:
    return await db.fetch_all("transaction", {"user_id": user_id})


async def get_all_transactions() -> list[dict[str, Any]]:
    return await db.fetch_all("transaction", {})


async def create_transaction(transaction_data: TransactionCreate, user_id: str) -> stripe.checkout.Session:
    stripe.api_key = checkout_config.STRIPE_API_KEY
    order_id = transaction_data.order_id
    if await get_transaction_by_order_id(order_id):
        raise TransactionAlreadyExists()

    # transaction = Transaction(
    #     created_at=transaction_data.created_at,
    #     order_id=order_id,
    #     payment_info=transaction_data.payment_info,
    #     status=TransactionStatus.PENDING,
    #     amount=amount
    # )

    try:
        session = stripe.checkout.Session.create(
            line_items=await get_line_items_by_order_id(order_id),
            mode="payment",
            success_url=app_config.FRONTEND_HOST + f":{app_config.FRONTEND_PORT}/checkout/result?success=true",
            cancel_url=app_config.FRONTEND_HOST + f":{app_config.FRONTEND_PORT}/checkout/result?canceled=true",
        )
        transaction = Transaction(
            created_at=transaction_data.created_at,
            order_id=order_id,
            user_id=user_id,
            stripe_session_id=session.id,
            status=TransactionStatus.COMPLETED, # COMPLETED for now
            amount=await get_amount_by_order_id(order_id),
        )
        await save_transaction(transaction)
        return session
    except stripe.error.StripeError as e:
        raise StripeError(e.user_message) from e


async def fulfill_transaction(session_id: str):
    print("Fulfilling checkout session", session_id)

    # Retrieve the checkout session
    try:
        checkout_session = stripe.checkout.Session.retrieve(
            session_id,
            # expand=["line_items"]
        )
    except stripe.error.StripeError as e:
        raise StripeError(e.user_message) from e

    # Check if payment is already succeeded for this Checkout Session
    transaction = await get_transaction_by_session_id(session_id)
    if transaction and transaction["status"] == TransactionStatus.COMPLETED.value:
        raise TransactionAlreadySuccessful()

    if checkout_session.payment_status != 'unpaid':
        # Fulfill the purchase...
        await db.execute(
            "transaction",
            {"filter": {"stripe_session_id": session_id}, "update": {"$set": {"status": TransactionStatus.COMPLETED.value}}},
            "update"
        )
        print("Payment was successful.")
    else:
        await db.execute(
            "transaction",
            {"filter": {"stripe_session_id": session_id}, "update": {"$set": {"status": TransactionStatus.FAILED.value}}},
            "update"
        )
        print("Payment was not successful.")
