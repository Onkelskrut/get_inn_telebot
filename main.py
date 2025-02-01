import telebot
import dadata
import requests
import json
from dadata import Dadata
from telebot import types
# from keys import TOKEN, SECRET_KEY, DADATA_TOKEN
import os


# getting environment variables
TOKEN = os.getenv('BOT_TOKEN_GET_INN')
SECRET_KEY = os.getenv('SECRET_KEY_GET_INN')
DADATA_TOKEN = os.getenv('DADATA_TOKEN')

# configuring the bot and connecting to the api


bot = telebot.TeleBot(TOKEN)
dadata_token = DADATA_TOKEN
secret = SECRET_KEY

my_dadata = Dadata(dadata_token, secret)

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Введите ИНН организации')

@bot.message_handler(func=lambda message: True)
def return_org(message):
    inn = message.text
    headers = {"Content-Type": "application/json", "Authorization": "Token {}".format(dadata_token)}
    response = requests.post('https://dadata.ru/api/v2/suggest/party', headers=headers, json={"query": inn})
    data = response.json()
    if not data['suggestions']:
        bot.send_message(message.chat.id, 'ИНН не найден')
        return
    org_name = data['suggestions'][0]['value']
    value = data['suggestions'][0]['data']['address']['value']
    link = f"https://www.rusprofile.ru/search?query={inn}"
    bot.reply_to(message, f"Название организации: {org_name}\nЮридический адрес: {value}\nИНН: {inn}\n{link}")

bot.polling(none_stop=True)


# bik module in progress

# @bot.message_handler(func=lambda message: True)
# def return_bik(message):
#     inn = message.text
#     headers = {'Content-Type': 'application/json', 'Authorization': 'Token {}'.format(dadata_token)}
#     response = requests.post('http://suggestions.dadata.ru/suggestions/api/4_1/rs/findById/bank', headers= headers, json={"query": inn})
#     print(f"response: {response}")
#     data = response.json()
#
#
#     if not data['suggestions']:
#         bot.send_message(message.chat.id, 'ИНН не найден')
#         return
#
#     bik = data['suggestions'][0]['data']['bic']
#     bot.reply_to(message, f'БИК : {bik}')
