import requests
from datetime import datetime
from pprint import pprint as pp
from config import CRYPTO_API, CRYPTO_IDS, CRYPTO_VS_CURRENCY

def fetch_bitcoin_price():
    try:
        url = CRYPTO_API
        params = {
            "ids": CRYPTO_IDS,
            "vs_currencies": CRYPTO_VS_CURRENCY
        }
        response = requests.get(url, params=params)
        response.raise_for_status()

        data = response.json()
        price = data[CRYPTO_IDS][CRYPTO_VS_CURRENCY]

        result = {
            "timestamp": datetime.utcnow().isoformat(),
            "price": price
        }

        return result

    except requests.RequestException as e:
        print(f"❌ Error fetching price from CoinGecko: {e}")
        return None
