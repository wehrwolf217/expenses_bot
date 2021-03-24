#!/usr/bin/env python
# -*- coding: utf-8 -*-
import configparser
import datetime

import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from data_base_queries import insert, output_data

config = configparser.ConfigParser()
config.read('Token.ini')

token = config['bot']['token']  # введите свой токен
bot = telebot.TeleBot(token)

data_list = []
list_of_expenses = ["еда", "проезд", "сигареты", "прочее", "комуналка"]
reciepts_list = ["зарплата", 'левак', 'родители']


# простая заглушка чтоб обрабатывать сообщения только от конкретного пользователя(либо несколько пользователей
# message.from_user.id not in some_data
@bot.message_handler(func=lambda message: int(message.from_user.id) != впишите свой id)
def some(message):
    bot.send_message(message.chat.id, 'ты не мой создатель, отвали!')


@bot.message_handler(commands=['start'])
def bot_start(message):
    bot.send_message(message.chat.id,
                     f'hello {message.from_user.first_name} введите цифру или /output для '
                     f'отображения статистики по месяцу')


@bot.message_handler(commands=['output'])
def output(message):
    date = datetime.datetime.now().strftime("%m-%Y")
    msg = output_data(f'%{date}')
    bot.send_message(message.chat.id, f'{msg}')


@bot.message_handler(content_types='text')
def check_input(message):
    try:
        user_sum_input = float(message.text)
        bot.send_message(message.chat.id, 'выберите куда зачислить', reply_markup=table_markup())
        date = datetime.datetime.now().strftime("%d-%m-%Y")
        data_list.append(date)
        data_list.append(user_sum_input)
        if len(data_list) > 2:
            bot.send_message(message.chat.id,
                             "вы ввели более 1го значения затрат/доходов, я обрабатываю только по 1й записи"
                             "повторите ввод")
            data_list.clear()

    except Exception as exp:
        bot.send_message(message.chat.id, 'я регистрирую только числа, введи число')
        print(exp)


@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data == 'рассходы':
        bot.send_message(call.message.chat.id, 'на что потратил?', reply_markup=type_expenses_markup())
    elif call.data in list_of_expenses:
        write_to_db('expenses', data_list, call.data)
        bot.send_message(call.message.chat.id, "запись успешно добавлена")
        data_list.clear()
    elif call.data == "доходы":
        bot.send_message(call.message.chat.id, 'откуда деньги?', reply_markup=type_receipts_markup())
    elif call.data in reciepts_list:
        write_to_db('receipts', data_list, call.data)
        bot.send_message(call.message.chat.id, "запись успешно добавлена")
        data_list.clear()


def table_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("рассходы 💰📉", callback_data="рассходы"),
               InlineKeyboardButton("доходы 💰📈", callback_data="доходы"))
    return markup


def type_expenses_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton('еда 🍲', callback_data="еда"),
               InlineKeyboardButton('проезд 🚎', callback_data="проезд"),
               InlineKeyboardButton('сигареты 🚬', callback_data="сигареты"),
               InlineKeyboardButton('прочее 🛒', callback_data="прочее"),
               InlineKeyboardButton('комуналка 🛁', callback_data="комуналка"))
    return markup


def type_receipts_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton('зарплата 💳', callback_data="зарплата"),
               InlineKeyboardButton('левак 🗳', callback_data='левак'),
               InlineKeyboardButton('родители 🤝', callback_data='родители'))
    return markup


def write_to_db(table_name: str, list_of_data: list, call_data: str):
    list_of_data.append(call_data)
    return insert(table_name, tuple(list_of_data))


while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)
        pass
        print('нужен был перезапуск для пользователя')
