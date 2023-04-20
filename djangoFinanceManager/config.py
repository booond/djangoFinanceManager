import requests

with requests.get('https://api.coingecko.com/api/v3/coins/list') as response:
    coins_list = response.json()
