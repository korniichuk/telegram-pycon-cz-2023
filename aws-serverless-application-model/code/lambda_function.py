#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Name: lambda_function
# Description: Echo bot with python-telegram-bot
# Version: 0.1a3
# Owner: Ruslan Korniichuk

import os
import json

from telegram.ext import Dispatcher, MessageHandler, Filters
from telegram import Update, Bot


TOKEN = os.environ['TOKEN']

bot = Bot(token=TOKEN)
dispatcher = Dispatcher(bot, None, use_context=True)


def echo_message(update, context):
    chat_id = update.message.chat_id
    chat_text = update.message.text

    context.bot.send_message(chat_id=chat_id, text=chat_text)


def lambda_handler(event, context):
    dispatcher.add_handler(MessageHandler(Filters.text, echo_message))

    try:
        dispatcher.process_update(
            Update.de_json(json.loads(event["body"]), bot)
        )

    except Exception as e:
        print(e)
        return {"statusCode": 500}

    return {"statusCode": 200}
