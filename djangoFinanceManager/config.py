import requests


def convert_list_to_dict(ls):
    return {coin["id"]: coin["symbol"] for coin in ls}


with requests.get('https://api.coingecko.com/api/v3/coins/list') as response:
    coins_dict = convert_list_to_dict(response.json())


