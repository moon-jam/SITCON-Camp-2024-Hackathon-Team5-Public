import os
import telebot
from config import telegram_token

from tools.help import send_welcome
from tools.schedule import handle_location
from tools.picture import send_elder_picture, color, callback_query_color
from tools.calendar_ import set_calendar_link, set_calendar_notify, today, start
from tools.weather import callback_query, weather

bot = telebot.TeleBot(telegram_token)

text_color = "0xffffff"

@bot.message_handler(commands=['picture'])
def _send_elder_picture(message):
    send_elder_picture(message, bot)

@bot.message_handler(commands=['color'])
def _color(message):
    color(message, bot)

@bot.callback_query_handler(func=lambda call: call.data in ['red', 'pink', 'yellow', 'dark blue', 'light blue', 'purple', 'white', 'black', 'gray', 'orange'])
def _callback_query_color(call):
    callback_query_color(call, bot)

@bot.callback_query_handler(func=lambda call: True)
def _callback_query(call):
    callback_query(call, bot)

@bot.message_handler(commands=['help'])
def _send_welcome(message):
    send_welcome(message, bot)

@bot.message_handler(content_types=['location'])
def _handle_location(message):
    handle_location(message, bot)

@bot.message_handler(commands=["set_calendar_link"])
def _set_calendar_link(message):
    set_calendar_link(message, bot)

@bot.message_handler(commands=["set_calendar_notify"])
def _set_calendar_notify(message):
    set_calendar_notify(message, bot)

@bot.message_handler(commands=["calendar_today"])
def _today(message):
    today(message, bot)

@bot.message_handler(commands=["start"])
def _start(message):
    send_welcome(message, bot)
    start(message, bot)

@bot.callback_query_handler(func=lambda call: call.data.startswith('county_') or call.data.startswith('sitename_'))
def _callback_query(call):
    callback_query(call, bot)

@bot.message_handler(commands=['weather'])
def _weather(message):
    weather(message, bot)

bot.infinity_polling()