# DRC_TRANSACTIONS/services.py
# API EXTERNE

import requests
from django.conf import settings

def get_currency_conversion(from_currency, to_currency, amount):
    url = f"{settings.GETGEOAPI_BASE_URL}?api_key={settings.GETGEOAPI_KEY}&from={from_currency}&to={to_currency}&amount={amount}&format=json"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()
