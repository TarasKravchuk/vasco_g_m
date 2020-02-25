from .views import add_currency_rates, CurrencyList, separately_currency, currency_deleter, redirect_main_page
from django.urls import path

app_name = 'vasco_engine'

urlpatterns = [
    path('', CurrencyList.as_view(), name='vasco'),
    path('add/', add_currency_rates, name='add_currency'),
    path('delete/<int:id>/', currency_deleter, name='object_deleter'),
    path('<str:currency>/', separately_currency, name='personal_currency'),
]
