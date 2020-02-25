from django.db import models
from django.core.validators import MinValueValidator
# Create your models here.

class CurrencyRatesModel (models.Model):
    id = models.AutoField(primary_key=True)
    currency_list = (
        ('USD', 'usd'),
        ('EUR', 'eur'),
        ('JPY', 'jpy'),
        ('HUF', 'huf'),
        ('CHF', 'chf'),)

    currency = models.CharField(max_length=3, choices=currency_list, default='USD')
    purchase_rate = models.FloatField(validators=[MinValueValidator(0.000000000001)])
    sale_rate = models.FloatField(validators=[MinValueValidator(0.000000000001)])
    valid_from = models.DateField()
    valid_till = models.DateField()

    class Meta:
        ordering = ('-valid_from',)

    def __str__ (self):
        return f"{self.valid_from} {self.valid_till} {self.currency} {self.purchase_rate} {self.sale_rate}"

