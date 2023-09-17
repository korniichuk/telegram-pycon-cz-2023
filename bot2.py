#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Name: bot2
# Description: Synchronous NBP bot with pyTelegramBotAPI
# Version: 0.1a7
# Owner: Ruslan Korniichuk

import os

from dotenv import load_dotenv
import telebot
from telebot.types import (
        InlineKeyboardButton,
        InlineKeyboardMarkup,
        InlineQueryResultArticle,
        InputTextMessageContent)

from nbp import get_rate, get_table

load_dotenv()
TOKEN = os.getenv('TOKEN')

bot = telebot.TeleBot(TOKEN, parse_mode='Markdown')

markup = InlineKeyboardMarkup()
a = InlineKeyboardButton('table A', callback_data='a')
b = InlineKeyboardButton('table B', callback_data='b')
c = InlineKeyboardButton('table C', callback_data='c')
markup.row(a, b, c)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "🔥 Hello, World!", reply_markup=markup)


@bot.message_handler(commands=['a', 'b', 'c'])
def tables_command(message):
    command = message.text[1]
    bot.send_message(message.chat.id, get_table(command))


@bot.callback_query_handler(func=lambda call: True)
def callback_querry(call):
    bot.send_message(call.message.chat.id, get_table(call.data))


@bot.inline_handler(lambda query: query.query == 'rate')
def inline(inline_query):
    r1 = InlineQueryResultArticle(
            '1', 'USD', InputTextMessageContent(
                    get_rate('usd'), parse_mode='Markdown'))
    r2 = InlineQueryResultArticle(
            '2', 'EUR', InputTextMessageContent(
                    get_rate('eur'), parse_mode='Markdown'))
    r3 = InlineQueryResultArticle(
            '3', 'GBP', InputTextMessageContent(
                    get_rate('gbp'), parse_mode='Markdown'))

    # cache_time -- maximum amount of time in seconds that result of
    # inline query may be cached on server
    bot.answer_inline_query(inline_query.id, [r1, r2, r3], cache_time=1)


bot.delete_webhook()
bot.infinity_polling()
