from extensions import *

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def start_help(message:telebot.types.Message):
    text = command_str['/help']
    if message.text == '/start':
        text = command_str['/start'] + text
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = command_str['/values'] +  "\n".join(x + " - " + curr_list[x] for x in curr_list.keys())
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    text = converter.convert(message)
    bot.send_message(message.chat.id, text)

bot.polling()