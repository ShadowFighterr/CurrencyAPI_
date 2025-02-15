from django.db import models
from django.utils.timezone import now

class ExchangeRate(models.Model):
    base_currency = models.CharField(max_length=3, default="USD")
    target_currency = models.CharField(max_length=3)
    rate = models.DecimalField(max_digits=10, decimal_places=4)
    last_updated = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.base_currency} to {self.target_currency}: {self.rate}"
