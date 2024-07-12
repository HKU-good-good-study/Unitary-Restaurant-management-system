from os import getenv

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class CheckoutConfig(BaseSettings):
    STRIPE_API_KEY: str = getenv("STRIPE_API_KEY")
    STRIPE_WEBHOOK_SECRET: str = "whsec_..."


checkout_config = CheckoutConfig()
