import telebot
import dadata
import requests
import json
from dadata import Dadata
from telebot import types

bot = telebot.TeleBot('7731839807:AAG3gKELPKJdDu0WgHPpg-RApo04GxnwIBU')
dadata_token = '877d125aeebbc6f111a42cb4bf7f21fc9bb27a3b'
secret = "2aea8167ef719c5f8a4a0302dd82ca85da2f1126"

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

def return_bik(message):
    inn = message.text
    headers = {'Content-Type': 'application/json', 'Authorization': 'Token {}'.format(dadata_token)}
    response = requests.post('http://suggestions.dadata.ru/suggestions/api/4_1/rs/suggest/bank', headers= headers, json={inn})
    data = response.json()

    if not data['suggestions']:
        bot.send_message(message.chat.id, 'ИНН не найден')
        return

    bik = data['suggestions'][0]
    bot.reply_to(message, f'это БИК : {bik}')

bot.polling(none_stop=True)

