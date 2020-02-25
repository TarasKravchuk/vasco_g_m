from django.test import TestCase
from .models import CurrencyRatesModel
from datetime import datetime, date
from .validators import ensuring_continuity, ensuring_deleter



# Create your tests here.

class CurrencyTestCase(TestCase):
    def test_add_currency(self):

        CurrencyRatesModel(currency='USD', purchase_rate=24.2, sale_rate=24.9,
                              valid_from=datetime.today(), valid_till=datetime.today()).save()

        new_object = CurrencyRatesModel(currency='USD', purchase_rate=24.2, sale_rate=24.9,
                                          valid_from=datetime.strptime('01/01/2020', '%d/%m/%Y'),
                                              valid_till=datetime.strptime('01/01/2020', '%d/%m/%Y'))
        ensuring_continuity(CurrencyRatesModel, new_object)
        new_object.save()

        self.assertEqual(CurrencyRatesModel.objects.get(currency='USD', valid_from=datetime.strptime('02/01/2020', '%d/%m/%Y') ).valid_till,
                         (date.today()))

        new_object_for_delete = CurrencyRatesModel(currency='USD', purchase_rate=24.2, sale_rate=24.9,
                                          valid_from=datetime.strptime('05/01/2020', '%d/%m/%Y'),
                                              valid_till=datetime.strptime('07/01/2020', '%d/%m/%Y'))

        ensuring_continuity(CurrencyRatesModel, new_object_for_delete)
        new_object_for_delete.save()

        self.assertEqual(CurrencyRatesModel.objects.get(currency='USD', valid_from=datetime.strptime('02/01/2020',
                                                   '%d/%m/%Y')).valid_till, datetime.strptime('04/01/2020', '%d/%m/%Y').date())

        ensuring_deleter(CurrencyRatesModel, new_object_for_delete)


        self.assertEqual(CurrencyRatesModel.objects.get(currency='USD', valid_from=datetime.strptime('02/01/2020',
                                           '%d/%m/%Y')).valid_till, (datetime.strptime('07/01/2020', '%d/%m/%Y').date()))


