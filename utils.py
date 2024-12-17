import requests
from config import lst


class ConvertException(Exception):
    pass

class СurrencyConvert:
    @staticmethod
    def convert(quote: str, base: str, amount: str):
        if quote == base:
            raise ConvertException(f'Не возможно перевести одинаковые валюты {base}')

        if quote not in lst:
            raise ConvertException(f'Не удалось обработать валюту {quote}\nпроверьте правильность ввода')

        if base not in lst:
            raise ConvertException(f'Не удалось обработать валюту {base}\nпроверьте правильность ввода')

        try:
            amount_ticker = float(amount)
        except:
            raise ConvertException(f'Не удалось обработать колличество валюты {amount}')

        r = requests.get(f'https://v6.exchangerate-api.com/v6/c2c2896e3173435484c8f038/latest/{quote}')
        total_base = r.json()
        res = amount_ticker * float(total_base['conversion_rates'][base])
        return f"{res:.3f}"

