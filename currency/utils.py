import requests
from django.core.cache import cache
from datetime import timedelta

CACHE_KEY = 'exchange_rates'
CACHE_TIMEOUT = 2 * 60 * 60  # 2 hours in seconds

def fetch_exchange_rates():
    # Check if rates exist in cache
    rates = cache.get(CACHE_KEY)
    if rates:
        return rates

    # Otherwise, fetch from external API (replace URL and params with your API's details)
    response = requests.get('https://api.exchangeratesapi.io/latest')
    if response.status_code == 200:
        rates = response.json()
        # Cache the rates
        cache.set(CACHE_KEY, rates, CACHE_TIMEOUT)
        return rates
    else:
        raise Exception('Failed to fetch exchange rates')
