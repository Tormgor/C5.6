import telebot
from config import keys, TOKEN # запрос в конфигурационый файл
from extensions import APIException, Converter


bot = telebot.TeleBot(TOKEN)

#обработка комманд старт и помощь
@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Вы работаете с Telegram ботом. \nЕго функционал, это конвертация валют. \nСписок доступных валют для ' \
           'конвертации: /values \nФормат запроса: валюта№1 валюта№2 количество '
    bot.reply_to(message, text)
    
#обработка команды варианты валют
@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)
    
#обработка резульатов работы
@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    values = message.text.split(' ')
    values = list(map(str.lower, values))
    try:
        total_base = Converter.get_price(values)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя \n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду. \n{e}')
    else:
        text = f'Цена {values[2]} {values[0]} в {values[1]} = {total_base} {values[1]}'
        print(total_base)
        bot.reply_to(message, text)

bot.polling(none_stop=True, interval=0)
