from checkout.constants import ErrorCode
from exceptions import BadRequest, NotFound, ServiceUnavailable


class OrderIdRequired(BadRequest):
    DETAIL = ErrorCode.ORDER_ID_REQUIRED


class OrderNotFound(NotFound):
    DETAIL = ErrorCode.ORDER_NOT_FOUND


class PaymentInformationRequired(BadRequest):
    DETAIL = ErrorCode.PAYMENT_INFORMATION_REQUIRED


class TransactionDataRequired(BadRequest):
    DETAIL = ErrorCode.TRANSACTION_DATA_REQUIRED


class TransactionAlreadyExists(BadRequest):
    DETAIL = ErrorCode.TRANSACTION_ALREADY_EXISTS


class TransactionAlreadySuccessful(BadRequest):
    DETAIL = ErrorCode.TRANSACTION_ALREADY_SUCCESSFUL


class StripeError(ServiceUnavailable):
    DETAIL = ErrorCode.STRIPE_ERROR

    def __init__(self, message: str | None = None):
        super().__init__()
        if message:
            self.DETAIL = message


class CheckoutParamInvalid(BadRequest):
    DETAIL = "Invalid request."
