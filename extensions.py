import requests
import json
from config import keys # запрос в конфигурационый файл

class APIException(Exception):
    pass

# класс обработки состояний
class Converter:
    @staticmethod
    def get_price(values):
        if len(values) != 3:
            raise APIException('Неправильный запрос! Введите три параметра, две валюты и число.')
        quote, base, amount = values
        if quote == base:
            raise APIException(f'Вы указали одинаковые валюты для конвертации.')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Укажите валюту из списка /values, Вы запросили {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Укажите валюту из списка /values, Вы запросили {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Конвертация работает с целыми значения валют, вы запросили: {amount}')

# запрос к API конвертации. ключ к API с бесплатной подписки
# Примечание. Данный api c сайта https://exchangeratesapi.io/  показывает только пары EUR-валюта2(для бесплатной подписки), для этого при
# ситуации валюта1-EUR, мы переварачиваем значения.

        request = requests.get('http://api.exchangeratesapi.io/v1/latest?access_key=e1ad57b79b9c51d86b808dbee237d1db')
        result = json.loads(request.content)
        money_dict = result['rates']
        v1 = money_dict[base_ticker]
        v2 = money_dict[quote_ticker]
        if quote_ticker == "EUR":
            total_base = v1 * amount
        else:
            total_base = (v1/v2) * amount


        return round ( total_base, 2)
