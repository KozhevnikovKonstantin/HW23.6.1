import json

import requests
from config import keys


class ConversionException(Exception):
    pass

class CurrencyConverter:
    @staticmethod
    def convert(base: str, quote: str, amount: str):
        if quote == base:
            raise ConversionException(f"Нельзя конвертировать одинаковые вылюты {quote}")
        try:
            keys[base]
        except KeyError:
            raise ConversionException(f"Не удалось обработать валюту {base}")
        try:
            keys[quote]
        except KeyError:
            raise ConversionException(f"Не удалось обработать валюту {quote}")
        try:
            amount = float(amount)
            if amount < 0:
                raise ConversionException("Невозможно конвертировать отрицательное количество валюты")
        except ValueError:
            raise ConversionException(f"Не удалось обработать количество {amount}")
        base_ticker, quote_ticker = keys[base], keys[quote]
        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={base_ticker}&tsyms={quote_ticker}')
        total_base = json.loads(r.content)[keys[quote]]
        total_base = round(float(total_base)*float(amount), 2)
        return  str(total_base)