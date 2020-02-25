from .models import CurrencyRatesModel
from django.forms import ModelForm


class CurrencyRatesForm (ModelForm):
    class Meta:
        model = CurrencyRatesModel
        fields = ['currency', 'purchase_rate', 'sale_rate', 'valid_from', 'valid_till']
