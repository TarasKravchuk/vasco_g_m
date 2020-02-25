from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from .models import CurrencyRatesModel
from .forms import CurrencyRatesForm
from .validators import valid_dates, valid_rates, ensuring_continuity, ensuring_deleter
from django.views.generic import ListView
from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage

# Create your views here.

def redirect_main_page(request):
    return redirect('/rates/')

def add_currency_rates (request):
    title = 'add new currency rates'
    form = CurrencyRatesForm()
    if request.method == 'POST':
        currency_form = CurrencyRatesForm(data=request.POST)
        if currency_form.is_valid():
            new_currency_rate = currency_form
            new_currency_rate = new_currency_rate.save(commit=False)
            if valid_dates(new_currency_rate.valid_from, new_currency_rate.valid_till) and valid_rates(new_currency_rate.purchase_rate, new_currency_rate.sale_rate):
                ensuring_continuity(CurrencyRatesModel, new_currency_rate)
                new_currency_rate.save()
                return redirect('/rates/')
            else:
                return render(request, 'vasco_engine/rates_list.html', {'form': form, 'title': title})
    return render(request, 'vasco_engine/rates_list.html', {'form': form, 'title': title})


class CurrencyList (ListView):
    queryset = CurrencyRatesModel.objects.all().order_by('-valid_till')
    paginate_by =10
    context_object_name = 'rates_list'
    template_name = 'vasco_engine/main_page.html'

def separately_currency(request, currency:str):
    title = currency
    currency_list = get_list_or_404(CurrencyRatesModel, currency=currency)
    paginator = Paginator(currency_list, 10)
    page = request.GET.get('page')
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)
    content = {'rates_list': currency_list, 'title': title, 'post_list': post_list}
    return render(request, 'vasco_engine/personal_currency_page.html', content)

def currency_deleter(request, id):
    object_for_delete = get_object_or_404(CurrencyRatesModel, id=int(id))
    ensuring_deleter(CurrencyRatesModel, object_for_delete)
    return redirect('/rates/')
