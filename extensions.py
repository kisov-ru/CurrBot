import telebot
import requests
import json
from config import *

class BotException(Exception):
    pass

class converter():
    @staticmethod
    def get_price(base:str, quote:str, amount:float)->float:
        req_res = requests.get(web_api_str.format(base, quote))
        total_base = json.loads(req_res.content)[quote]
        return round(total_base * amount, 2)

    @staticmethod
    def convert(message: telebot.types.Message) -> str:
        try:
            params = message.text.split()
            if len(params) != 3:
                raise BotException('Должно быть три аргумента /help')
            base,quote,amount = params
            base = base.upper()
            quote = quote.upper()
            if not base in curr_list.keys():
                raise BotException(f'Валюты {base} нет в списке /values')
            if not quote in curr_list.keys():
                raise BotException(f'Валюты {quote} нет в списке /values')
            if quote == base:
                raise BotException(f'Выберите разные валюты /values')

            amount = float(amount)
            price = converter.get_price(base, quote, amount)
            return f'{amount} {curr_list[base]} = {price} {curr_list[quote]}'

        except Exception as e:
            ex_name = type(e).__name__
            if ex_name == 'ValueError':
                text_error = f'Ошибка конвертации количества - {amount}'
            elif ex_name == 'ConnectionError':
                text_error = 'Сайт недоступен'
            else:
                text_error = e

            return f'Ошибка типа {type(e).__name__}: {text_error}'


