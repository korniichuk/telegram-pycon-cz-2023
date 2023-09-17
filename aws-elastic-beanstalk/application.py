#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Name: application
# Description: "Hello, World!" and echo bot with pyTelegramBotAPI
# Version: 0.1a2
# Owner: Ruslan Korniichuk

import os
import time

from flask import Flask, request
import telebot

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)
application = Flask(__name__)


@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(message, "🔥 Hello, World!")


@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, message.text)


@application.route('/' + TOKEN, methods=["POST"])
def get_message():
    json_string = request.get_data().decode("utf-8")
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return '!', 200


@application.route('/')
def webhook():
    time.sleep(1)
    url = "https://korniichuk.click/" + TOKEN
    bot.set_webhook(url)
    return '!', 200


if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()
