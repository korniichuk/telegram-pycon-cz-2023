#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Name: bot4
# Description: Asynchronous NBP bot with python-telegram-bot
# Version: 0.1a5
# Owner: Ruslan Korniichuk

import os

from dotenv import load_dotenv
from telegram import (
        InlineKeyboardButton,
        InlineKeyboardMarkup,
        InlineQueryResultArticle,
        InputTextMessageContent,
        Update)
from telegram.ext import (
        ApplicationBuilder,
        CallbackQueryHandler,
        CommandHandler,
        ContextTypes,
        InlineQueryHandler)

from nbp import get_rate, get_table

load_dotenv()
TOKEN = os.getenv('TOKEN')

a = InlineKeyboardButton('table A', callback_data='a')
b = InlineKeyboardButton('table B', callback_data='b')
c = InlineKeyboardButton('table C', callback_data='c')
markup = InlineKeyboardMarkup([[a, b, c]])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="🔥 Hello, World!",
                                   reply_markup=markup)


async def tables_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    command = update.message.text[1]
    await context.bot.send_message(
            chat_id=update.effective_chat.id, text=get_table(command),
            parse_mode='Markdown')


async def tables_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await context.bot.send_message(
            chat_id=update.effective_chat.id, text=get_table(query.data),
            parse_mode='Markdown')


async def inline(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
    await context.bot.answer_inline_query(
            update.inline_query.id, [r1, r2, r3], cache_time=1)


if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    abc_handler = CommandHandler(['a', 'b', 'c'], tables_command)
    application.add_handler(abc_handler)

    application.add_handler(CallbackQueryHandler(tables_callback))

    # re.match() is used
    application.add_handler(InlineQueryHandler(inline, pattern='rate'))

    application.run_polling()
