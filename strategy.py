# strategy.py
import os
from dotenv import load_dotenv
import requests

load_dotenv()

API_KEY = os.getenv("TWELVE_DATA_API_KEY")
BASE_URL = "https://api.twelvedata.com"

def get_4h_candle():
    params = {
        "symbol": "EUR/USD",
        "interval": "4h",
        "apikey": API_KEY,
        "outputsize": 10,
    }
    response = requests.get(f"{BASE_URL}/time_series", params=params)
    response.raise_for_status()
    data = response.json()
    candles = data.get("values", [])
    for candle in candles:
        if "21:00" in candle["datetime"]:
            return {
                "high": float(candle["high"]),
                "low": float(candle["low"]),
                "time": candle["datetime"]
            }
    # fallback if no candle found
    return {}

def get_current_price():
    params = {"symbol": "EUR/USD", "apikey": API_KEY}
    response = requests.get(f"{BASE_URL}/price", params=params)
    response.raise_for_status()
    data = response.json()
    return float(data["price"])
