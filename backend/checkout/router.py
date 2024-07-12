import stripe
from fastapi import APIRouter, Depends, Request

from backend.auth.jwt import parse_jwt_customer_or_dinning_room_staff_data, parse_jwt_admin_data
from backend.auth.schemas import JWTData
from backend.checkout import service
from backend.auth import service as auth_service
from backend.checkout.config import checkout_config
from backend.checkout.dependencies import valid_order_id, valid_transaction_data
from backend.checkout.exceptions import OrderNotFound, CheckoutParamInvalid
from backend.checkout.schemas import TransactionCreate, RedirectResponse, TransactionResponse, AdminTransactionResponse
from backend.exceptions import BadRequest

router = APIRouter(prefix="/checkout", tags=["Checkout"])
endpoint_secret = checkout_config.STRIPE_WEBHOOK_SECRET


@router.post("/new", response_model=RedirectResponse)
async def create_transaction(
    transaction_data: TransactionCreate = Depends(valid_transaction_data),
    jwt_data: JWTData = Depends(parse_jwt_customer_or_dinning_room_staff_data),
) -> RedirectResponse:
    user_id = jwt_data.user_id
    if session := await service.create_transaction(transaction_data, user_id):
        return RedirectResponse(url=session.url)


@router.post("/webhook")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get('stripe-signature')
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError:
        # Invalid payload
        raise BadRequest()
    except stripe.error.SignatureVerificationError:
        # Invalid signature
        raise BadRequest()

    if (event['type'] == 'checkout.session.completed' or
        event['type'] == 'checkout.session.async_payment_succeeded'):
        await service.fulfill_transaction(event['data']['object']['id'])

    return {"status": "success"}


@router.get("/me", response_model=list[TransactionResponse])
async def get_transactions(
    jwt_data: JWTData = Depends(parse_jwt_customer_or_dinning_room_staff_data),
) -> list[TransactionResponse]:
    user_id = jwt_data.user_id
    user = await auth_service.get_user_by_id(user_id)
    if not user:
        raise OrderNotFound()
    transactions = await service.get_transaction_by_user_id(user_id)
    return [
        TransactionResponse(
            created_at=transaction["created_at"],
            order_id=transaction["order_id"],
            status=transaction["status"],
            amount=transaction["amount"],
        )
        for transaction in transactions
    ]


@router.get("/all", response_model=list[AdminTransactionResponse])
async def get_all_transactions(
    jwt_data: JWTData = Depends(parse_jwt_admin_data),
) -> list[AdminTransactionResponse]:
    transactions = await service.get_all_transactions()
    return [
        AdminTransactionResponse(
            created_at=transaction["created_at"],
            order_id=transaction["order_id"],
            status=transaction["status"],
            amount=transaction["amount"],
            user_id=transaction["user_id"],
            stripe_session_id=transaction["stripe_session_id"],
        )
        for transaction in transactions
    ]
