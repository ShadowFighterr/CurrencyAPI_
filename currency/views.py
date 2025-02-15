from django.http import JsonResponse
from django.core.cache import cache
from .models import ExchangeRate
from rest_framework.throttling import UserRateThrottle
from rest_framework.decorators import api_view, throttle_classes

# Define a custom throttle class (200 requests per day per user)
class DailyRateThrottle(UserRateThrottle):
    rate = '200/day'  # Each user can only make 200 requests per day

@api_view(['GET'])
@throttle_classes([DailyRateThrottle])
def get_exchange_rates(request):
    # Try to get rates from cache
    cached_rates = cache.get("exchange_rates")
    if cached_rates:
        return JsonResponse(cached_rates)

    # If not cached, fetch from DB
    rates = ExchangeRate.objects.all()
    rates_data = {rate.target_currency: float(rate.rate) for rate in rates}

    # Store in cache for 2 hours (7200 seconds)
    cache.set("exchange_rates", {"base": "USD", "rates": rates_data}, timeout=7200)

    return JsonResponse({"base": "USD", "rates": rates_data})
