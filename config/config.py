import os
from sqlalchemy import create_engine


CRYPTO_API = "https://api.coingecko.com/api/v3/simple/price"
CRYPTO_IDS = "bitcoin"
CRYPTO_VS_CURRENCY = "usd"


class ConfigMgr:
    def __init__(self):
        pass

    def get_config(self):
        self.DB_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@database:5432/crypto_tracker")
        self.ENGINE = create_engine(self.DB_URL)

conf = ConfigMgr()
conf.get_config()      