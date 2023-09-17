#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Name: bot1
# Description: "Hello, World!" with pyTelegramBotAPI
# Version: 0.1a3
# Owner: Ruslan Korniichuk

import os

from dotenv import load_dotenv
import telebot

load_dotenv()
TOKEN = os.getenv("TOKEN")

bot = telebot.TeleBot(TOKEN, parse_mode=None)


@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(message, "🔥 Hello, World!")


bot.delete_webhook()
bot.infinity_polling()
