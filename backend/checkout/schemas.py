from datetime import date, datetime
from enum import Enum

from pydantic import field_validator, BaseModel
from pydantic_extra_types.payment import PaymentCardNumber

from models import CustomModel


class TransactionStatus(Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"


class PaymentInfo(BaseModel):
    card_number: PaymentCardNumber
    card_holder: str
    expiry_date: date
    cvv: str

    @field_validator("card_holder", mode="after")
    @classmethod
    def valid_card_holder(cls, card_holder: str) -> str:
        if not card_holder.replace(" ", "").isalpha():
            raise ValueError("Card holder name must contain only alphabets")

        return card_holder

    @field_validator("expiry_date", mode="after")
    @classmethod
    def valid_expiry_date(cls, expiry_date: date) -> date:
        if expiry_date < date.today():
            raise ValueError("Card has expired")

        return expiry_date

    @field_validator("cvv", mode="after")
    @classmethod
    def valid_cvv(cls, cvv: str) -> str:
        if not cvv.isdigit() or len(cvv) != 3:
            raise ValueError("CVV must be a 3-digit number")

        return cvv


class TransactionCreate(CustomModel):
    created_at: datetime = datetime.utcnow()
    order_id: str
    # payment_info: PaymentInfo


class Transaction(TransactionCreate):
    user_id: str
    stripe_session_id: str
    status: TransactionStatus
    amount: float


class TransactionResponse(TransactionCreate):
    status: TransactionStatus
    amount: float


class AdminTransactionResponse(TransactionResponse):
    user_id: str
    stripe_session_id: str


class RedirectResponse(BaseModel):
    url: str
