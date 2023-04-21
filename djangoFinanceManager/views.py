from django.shortcuts import render, redirect
from django.db.models import F
from .models import History, Cryptocurrencies
from .forms import PostForm, HistoryForm
from .config import coins_dict

import requests


def main(request):
    balance = 0
    expences = 0
    incomes = 0

    currencies_list = Cryptocurrencies.objects.all()
    history_list = History.objects.select_related('crypto_currency')

    link = 'https://api.coingecko.com/api/v3/simple/price?ids=' + \
           ','.join([currency.identificator for currency in currencies_list]) + \
           '&vs_currencies=usd'

    response = requests.get(link)
    if response.status_code == 200:
        data = response.json()
        for currency in currencies_list:
            item = data.get(currency.identificator)
            balance += item.get("usd") * float(currency.value)

        for x in history_list:
            if x.type == 'income':
                item = data.get(x.crypto_currency.identificator)
                incomes += float(x.amount) * item.get("usd")
            elif x.type == 'expense':
                item = data.get(x.crypto_currency.identificator)
                expences += float(x.amount) * item.get("usd")

    context = {"title": "Зведення",
               "balance": round(balance, 2),
               "incomes": round(incomes, 2),
               "expenses": round(expences, 2)}
    return render(request, 'djangoFinanceManager/main.html', context)


def history(request):
    history_list = History.objects.all()
    context = {"history": history_list, "title": "Історія"}
    return render(request, "djangoFinanceManager/history.html", context)


def currencies(request):
    crc = Cryptocurrencies.objects.all()
    context = {"crc": crc, "title": "Активи"}
    return render(request, "djangoFinanceManager/currencies.html", context)


def settings(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            identificator = request.POST.get('identificator')
            currency, created = Cryptocurrencies.objects.get_or_create(identificator=identificator)
            if not created:
                message = 'Error! This currency is already exists in your list.'
                response = redirect('settings')
                response.set_cookie('message', message, 1)
                return response
            else:
                item = coins_dict.get(identificator)
                if item:
                    currency.symbols = item["symbol"].upper()
                    currency.save()
                    message = 'Succesful added!'
                    response = redirect('settings')
                    response.set_cookie('message', message, 1)
                    return response
                else:
                    message = 'Error! This currency doesn\'t support.'
                    response = redirect('settings')
                    response.set_cookie('message', message, 1)
                    return response
    else:
        form = PostForm()
    context = {"form": form, "title": "Налаштування"}
    return render(request, "djangoFinanceManager/settings_page.html", context)


def add(request):
    if request.method == "POST":
        form = HistoryForm(request.POST)
        if form.is_valid():
            crypto_currency = form.cleaned_data['crypto_currency']
            value = form.cleaned_data['amount']
            tp = form.cleaned_data['type']

            if tp == 'income':
                Cryptocurrencies.objects.filter(id=crypto_currency.id).update(value=F('value') + value)
            elif tp == 'expense':
                if crypto_currency.value >= value:
                    Cryptocurrencies.objects.filter(id=crypto_currency.id).update(value=F('value') - value)
                else:
                    message = 'Error! You waste more, than you have.'
                    response = redirect('add')
                    response.set_cookie('message', message, 1)
                    return response
            form.save()
            message = 'Succesful added!'
            response = redirect('add')
            response.set_cookie('message', message, 1)
            return response
    else:
        form = HistoryForm()
    context = {"form": form, "title": "Додавання запису"}
    return render(request, "djangoFinanceManager/add_page.html", context)
