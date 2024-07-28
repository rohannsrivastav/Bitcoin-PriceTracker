# alerts/coingecko_api.py

import requests
import time
from django.conf import settings
from .models import Alert
from .utils import send_alert_email
class CoinGeckoAPI:
    def __init__(self):
        self.base_url = "https://api.coingecko.com/api/v3"
        self.endpoint = "/coins/markets"

    def fetch_prices(self):
        params = {
            "vs_currency": "inr",
            "order": "market_cap_desc",
            "per_page": 100,
            "page": 1,
            "sparkline": "false"
        }
        response = requests.get(f"{self.base_url}{self.endpoint}", params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error fetching data: {response.status_code}")
            return None

    def check_alerts(self, coin_data):
        for coin in coin_data:
            alerts = Alert.objects.filter(cryptocurrency=coin['symbol'].upper(), status='created')
            current_price = coin['current_price']
            for alert in alerts:
                if (alert.target_price >= current_price and alert.target_price > float(alert.initial_price)) or \
                   (alert.target_price <= current_price and alert.target_price < float(alert.initial_price)):
                    alert.status = 'triggered'
                    alert.save()
                    send_alert_email(alert, current_price)

    def run(self):
        while True:
            coin_data = self.fetch_prices()
            if coin_data:
                self.check_alerts(coin_data)
            time.sleep(60)  # Wait for 60 seconds before next API call

coingecko_api = CoinGeckoAPI()