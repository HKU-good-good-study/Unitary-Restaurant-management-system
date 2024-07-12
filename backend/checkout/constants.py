class ErrorCode:
    ORDER_ID_REQUIRED = "Order ID is required."
    ORDER_NOT_FOUND = "Order not found."
    PAYMENT_INFORMATION_REQUIRED = "Payment information is required."
    TRANSACTION_DATA_REQUIRED = "Transaction data is required."
    TRANSACTION_NOT_CREATED = "Transaction not created."
    TRANSACTION_ALREADY_EXISTS = "Transaction already exists."
    TRANSACTION_ALREADY_SUCCESSFUL = "Transaction is already successful."
    STRIPE_ERROR = "Failed to create payment."