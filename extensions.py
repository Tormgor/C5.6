import requests
import json
from config import keys, API_KEY # запрос в конфигурационого файла

class APIException(Exception):
    pass

# класс обработки состояний
class Converter:
    @staticmethod
    def get_price(values):
        if len(values) != 3:
            raise APIException('Неправильный запрос! Введити три параметра, валюты и число.')
        quote, base, amount = values
        if quote == base:
            raise APIException(f'Вы указали одинаковые валюты для конвертации.')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Укажите валюту из списка /values')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Укажите валюту из списка /values')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Конвертация работает с целыми значения валют, вы запросили: {amount}')

# запрос к api конвертации
        r = requests.get(f'http://api.exchangeratesapi.io/v1/latest?access_key={API_KEY}&base={quote_ticker}&symbols={base_ticker}')
        total_base = float(amount)*float(json.loads(r.content)["rates"][base_ticker])
        return round(total_base, 2)
