from django.shortcuts import render, redirect
from .models import History, Cryptocurrencies
from .forms import PostForm
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
    context = {"form": form, "title": "Історія"}
    return render(request, "djangoFinanceManager/settings_page.html", context)
