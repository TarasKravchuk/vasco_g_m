from datetime import timedelta
from .models import CurrencyRatesModel
from django.shortcuts import get_object_or_404

def valid_dates (valid_from, valid_till):
    if valid_till < valid_from:
        return False
    return True

def valid_rates (purchase_rate, sale_rate):
    if sale_rate < purchase_rate:
        return False
    return True

def ensuring_continuity (currency_list, new_currency_rate):
    value_inside = currency_list.objects.filter(currency=new_currency_rate.currency,
                                                valid_from__lte=new_currency_rate.valid_from,
                                                valid_till__gte=new_currency_rate.valid_till)
    if value_inside:
        new_value_before_new_currency_rate = CurrencyRatesModel(currency=new_currency_rate.currency,
                                                                purchase_rate=value_inside[0].purchase_rate,
                                                                sale_rate=value_inside[0].sale_rate,
                                                                valid_from=value_inside[0].valid_from,
                                                                valid_till=new_currency_rate.valid_from - timedelta(days=1))
        new_value_before_new_currency_rate.save()

        new_value_after_new_currency_rate = CurrencyRatesModel(currency=new_currency_rate.currency,
                                                               purchase_rate=value_inside[0].purchase_rate,
                                                               sale_rate=value_inside[0].sale_rate,
                                                               valid_from=new_currency_rate.valid_till + timedelta(days=1),
                                                               valid_till=value_inside[0].valid_till)
        new_value_after_new_currency_rate.save()

        value_inside.delete()
        return

    value_before = currency_list.objects.filter(currency=new_currency_rate.currency,
                                                       valid_from__gte=new_currency_rate.valid_from,
                                                       valid_till__gte=new_currency_rate.valid_till).order_by('valid_from')
    if value_before:
        new_value_before = CurrencyRatesModel(currency=new_currency_rate.currency,
                                                     purchase_rate=value_before[0].purchase_rate,
                                                     sale_rate=value_before[0].sale_rate,
                                                     valid_from=new_currency_rate.valid_till + timedelta(days=1),
                                                     valid_till=value_before[0].valid_till)
        value_before[0].delete()
        new_value_before.save()

        return

    value_inside_before = currency_list.objects.filter(currency=new_currency_rate.currency,
                                                       valid_from__gte=new_currency_rate.valid_from,
                                                       valid_from__lte = new_currency_rate.valid_till,
                                                       valid_till__gte=new_currency_rate.valid_till).order_by('valid_from')
    if value_inside_before:
        new_value_inside_before = CurrencyRatesModel(currency=new_currency_rate.currency,
                                                     purchase_rate=value_inside_before[0].purchase_rate,
                                                     sale_rate=value_inside_before[0].sale_rate,
                                                     valid_from=new_currency_rate.valid_till + timedelta(days=1),
                                                     valid_till=value_inside_before[0].valid_till)
        value_inside_before[0].delete()
        new_value_inside_before.save()

        return

    value_inside_after = currency_list.objects.filter(currency=new_currency_rate.currency,
                                                      valid_from__lte=new_currency_rate.valid_from,
                                                      valid_till__lte=new_currency_rate.valid_till).order_by('-valid_from')


    if value_inside_after:
        new_value_inside_after = CurrencyRatesModel(currency=new_currency_rate.currency,
                                                    purchase_rate=value_inside_after[0].purchase_rate,
                                                    sale_rate=value_inside_after[0].sale_rate,
                                                    valid_from=value_inside_after[0].valid_from,
                                                    valid_till=new_currency_rate.valid_from - timedelta(days=1))
        value_inside_after[0].delete()
        new_value_inside_after.save()

        return

def ensuring_deleter (currency_list, object_for_delete):
    object_before = currency_list.objects.filter(currency=object_for_delete.currency,
                                                 valid_till=object_for_delete.valid_from - timedelta(days=1))

    object_after = currency_list.objects.filter(currency=object_for_delete.currency,
                                                valid_from=object_for_delete.valid_till + timedelta(days=1))

    if list(object_before) != [] and list(object_after) != []:
        object_before[0].valid_till = object_after[0].valid_from - timedelta(days=1)
        object_before[0].save()
        object_for_delete.delete()

    else:
        object_for_delete.delete()
