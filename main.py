import telebot
from telebot import types

from config import keys, TOKEN
from utils import ConvertException, СurrencyConvert

bot = telebot.TeleBot(TOKEN)


def create_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    start_button = types.InlineKeyboardButton(text='Начало', callback_data='start')
    value_button = types.InlineKeyboardButton(text='Доступные валюты', callback_data='value')
    keyboard.add(start_button, value_button)
    return keyboard


@bot.message_handler(commands=['start', 'help', ])
def start(message: telebot.types.Message):
    text = (f'Бот для конвертации валюты\nЧто бы начать работу, введите команду в следующем формате:'
            f'\n<колличество валюты> <код валюты> <код валюты в какую перевести>'
            f'\nПример: 1000 rub usd'
            f'\nЧто бы посмотреть список и коды валют нажмите кнопку ниже или введите команду /value')
    bot.reply_to(message, text, reply_markup=create_keyboard())


@bot.message_handler(commands=['value',])
def value(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key, value in keys.items():
        text = '\n'.join((text, (f'{key} : {value}')))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:

        value1 = [item.upper().strip() for item in message.text.split(' ')]
        if len(value1) != 3:
            raise ConvertException('Не верный формат ввода!')

        amount, quote, base = value1
        total_base = СurrencyConvert.convert(quote, base, amount)
    except ConvertException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')

    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')

    else:
        text = f'Цена {amount} {quote} в {base} = {total_base}{base}'
        bot.reply_to(message, text, reply_markup=create_keyboard())

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "value":
        value(call.message)
    if call.data == "start":
        start(call.message)


bot.polling(none_stop=True)
