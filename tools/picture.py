
import os
import telebot
import random
import io
from telegram import Update, InputFile
from telegram.ext import Application, CommandHandler, CallbackContext
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from PIL import Image, ImageDraw, ImageFont
import google.generativeai as genai
from config import gemini_token, telegram_token
from datetime import datetime

# Access your API key as an environment variable.
genai.configure(api_key=gemini_token)

generation_config = {
    "temperature": 2,
    "top_p": 1,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}
no_safety_settings = [
    {
        "category": "HARM_CATEGORY_DANGEROUS",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE",
    },
]

model = genai.GenerativeModel(
    'gemini-1.5-flash',
    generation_config=generation_config,
    safety_settings=no_safety_settings
)

if os.path.exists('database/old_pictures/.DS_Store'):
    os.remove('database/old_pictures/.DS_Store')
    # 設定你的圖片路徑

if __name__ == '__main__':
    bot = telebot.TeleBot(telegram_token)

image_directory = './database/old_pictures/'

color2rgb = {
    "red" : [255, 0, 0],
    "pink" : [255, 0, 255],
    "yellow" : [255, 255, 0],
    "dark blue" : [25, 25, 112],
    "light blue" : [0, 255, 255],
    "purple" : [138, 43, 226],
    "white" : [255, 255, 255],
    "black" : [0, 0, 0],
    "gray" : [128, 128, 128],
    "orange" : [255, 165, 0]
}

def gen_markup():
    choice = ['紅色', '粉紅色', '黃色', '深藍色', '水藍色', '紫色', '白色', '黑色', '灰色', "橘色"]
    markup = InlineKeyboardMarkup()
    markup.row_width = 5
    markup.add(InlineKeyboardButton(choice[0], callback_data="red"),
                InlineKeyboardButton(choice[1], callback_data="pink"),
                InlineKeyboardButton(choice[2], callback_data="yellow"),
                InlineKeyboardButton(choice[3], callback_data="dark blue"),
                InlineKeyboardButton(choice[4], callback_data="light blue"),
                InlineKeyboardButton(choice[5], callback_data="purple"),
                InlineKeyboardButton(choice[6], callback_data="white"),
                InlineKeyboardButton(choice[7], callback_data="black"),
                InlineKeyboardButton(choice[8], callback_data="gray"),
                InlineKeyboardButton(choice[9], callback_data="orange"))
    return markup

# @bot.message_handler(commands=['color'])
def color(message, bot):
    bot.send_message(message.chat.id, "請輸入顏色", reply_markup=gen_markup())


text_color = "white"

# @bot.callback_query_handler(func=lambda call: True)
def callback_query_color(call, bot):
    global text_color
    text_color = call.data
    print(text_color)
    bot.send_message(call.message.chat.id, f"已設定顏色為 {text_color}")

# @bot.message_handler(commands=['picture'])
def send_elder_picture(message, bot):
    # https://ithelp.ithome.com.tw/articles/10247292
    all_files = os.listdir(image_directory)
    random_image_file = image_directory+random.choice(all_files)
    print(random_image_file)
    img = Image.open(random_image_file)
    backup_img = img.copy()
    draw = ImageDraw.Draw(backup_img)
    # draw.ink = (255, 165, 0)
    font = ImageFont.truetype('./font/Noto_Sans_TC/static/NotoSansTC-Black.ttf', 100 * img.size[1] // 750)
    text = ' ' + message.text[8:].strip()
    if text.strip() == '':
        prompt = (f"現在 {datetime.now().strftime("%H:%M")} (24小時制) 請生成一段十個字的問候")
        text  = model.generate_content(prompt).text
        print(text, text_color, color2rgb[text_color])
        draw.text( (0, 0), text, font=font, fill=(color2rgb[text_color][0], color2rgb[text_color][1], color2rgb[text_color][2]))
        # backup_img.show()

        backup_img.save('elder.jpg')

        bot.send_photo(message.chat.id, photo=open('elder.jpg', 'rb'))
    else:
        print(text, text_color, color2rgb[text_color])
        draw.text( (0, 0), text, font=font, fill=(color2rgb[text_color][0], color2rgb[text_color][1], color2rgb[text_color][2]))
        # backup_img.show()

        backup_img.save('elder.jpg')

        bot.send_photo(message.chat.id, photo=open('elder.jpg', 'rb'))

if __name__ == '__main__':

    @bot.message_handler(commands=['picture'])
    def _send_elder_picture(message):
        send_elder_picture(message, bot)
    
    
    @bot.message_handler(commands=['color'])
    def _color(message):
        color(message, bot)

    @bot.callback_query_handler(func=lambda call: True)
    def _callback_query_color(call):
        callback_query_color(call, bot)
    
    bot.infinity_polling()



