
import telebot

from config import telegram_token as TOKEN

if __name__ == "__main__":
    bot= telebot.TeleBot(TOKEN)

def send_welcome(message, bot):
    bot.reply_to(message, "What can this bot do? \
                        \n This bot will inform you about your day very well and will make your life much easier! \
                        \n /help - Get the list of commands \
                        \n /weather - Get the weather of a city \
                        \n /set_calendar_link [link] - Give the bot your username for your google calendar \
                        \n /calendar_today - Get the events of today \
                        \n /set_calendar_notify [time] - Set the time to notify you about the events of the day \
                        \n [location] - send your location, and the bot will tell you a today-schedule about the place near you \
                        \n /picture[sentence] - Get morning,noon and evening pictures \
                        \n /color - Change the word color in the picture ")
 
if __name__ == "__main__":

    @bot.message_handler(commands=['help', 'start'])
    def _send_welcome(message):
        send_welcome(message, bot)

    bot.infinity_polling()