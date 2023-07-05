import requests
import json

API_ID = '6fefb81eec25461a8fb8bc473a07e0f7'

def exchanger_currency():
    response = requests.get(f'https://openexchangerates.org/api/latest.json?app_id={API_ID}')

    data = json.loads(response.text)
    rates = data['rates']

    filter_rates = {
        'RUB': rates['RUB'],
        'KGS': rates['KGS'],
        'KZT': rates['KZT'],
        'TRY': rates['TRY'],
        'CNY': rates['CNY']
    }

    return filter_rates