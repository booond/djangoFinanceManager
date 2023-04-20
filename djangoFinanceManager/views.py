from django.shortcuts import render, redirect
from .models import History, Cryptocurrencies
from .forms import PostForm, HistoryForm
from .config import coins_list

import requests


def main(request):
    balance = 0
    link = ''
    currencies_values = Cryptocurrencies.objects.values_list()
    print(currencies_values)
    if currencies_values:
        link = 'https://api.coingecko.com/api/v3/simple/price?ids=' + currencies_values[0][1]
        if len(currencies_values) > 1:
            for currency in currencies_values[0:]:
                link += f'%2C{currency[1]}'
        link += '&vs_currencies=usd'
    print(link)
    response = requests.get(link)
    print(response)
    if response.status_code == 200:
        data = response.json()
        print(data)
        for currency in currencies_values:
            item = data.get(currency[1])
            balance += item.get("usd") * float(currency[3])
    else:
        data = {}
    print(data)

    context = {"title": "Зведення", "balance": round(balance, 2)}
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
            if Cryptocurrencies.objects.filter(identificator=identificator).exists():
                message = 'Error! This currency is already exists in your list.'
                response = redirect('settings')
                response.set_cookie('message', message, 1)
                return response
            else:
                for item in coins_list:
                    if item["id"] == identificator:
                        form.instance.symbols = item["symbol"].upper()
                        form.save()
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
            crypto_currency = request.POST.get('crypto_currency')
            value = float(request.POST.get('amount'))
            tp = request.POST.get('type')
            obj = Cryptocurrencies.objects.get(id=crypto_currency)
            if tp == 'income':
                result = float(obj.value) + value
                obj.value = result
            elif tp == 'expense':
                result = float(obj.value) - value
                if result >= 0:
                    obj.value = result
                else:
                    message = 'Error! You waste more, than you have.'
                    response = redirect('add')
                    response.set_cookie('message', message, 1)
                    return response
            obj.save()
            form.save()
            message = 'Succesful added!'
            response = redirect('add')
            response.set_cookie('message', message, 1)
            return response
    else:
        form = HistoryForm()
    context = {"form": form, "title": "Додавання запису"}
    return render(request, "djangoFinanceManager/add_page.html", context)
