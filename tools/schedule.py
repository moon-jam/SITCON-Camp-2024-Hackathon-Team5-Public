import os
import telebot
import google.generativeai as genai
from config import gemini_token, telegram_token
# import local

import requests
import xml.etree.ElementTree as ET

def get_address(longitude, latitude):
    # 替換{longitude}和{latitude}到URL中
    url = f"https://api.nlsc.gov.tw/other/TownVillagePointQuery/{longitude}/{latitude}/4326"
    response = requests.get(url)
    
    # 解析XML
    root = ET.fromstring(response.content)
    
    # 提取所需的地址信息
    ctyName = root.find('ctyName').text
    townName = root.find('townName').text
    officeName = root.find('officeName').text
    sectName = root.find('sectName').text
    villageName = root.find('villageName').text
    
    # 串接地址信息
    address = f"{ctyName}{townName}{officeName}{sectName}{villageName}"
    
    return address

if __name__ == "__main__":
    TOKEN = telegram_token
    bot = telebot.TeleBot(TOKEN, parse_mode=None)
    print("It's a beautiful day outside. Birds are singing, flowers are blooming...")

# Access your API key as an environment variable.
genai.configure(api_key=gemini_token)
# Choose a model that's appropriate for your use case.
model = genai.GenerativeModel('gemini-1.5-flash')


# @bot.message_handler(content_types=['location'])
def handle_location(message, bot):
    latitude = message.location.latitude
    longitude = message.location.longitude
    print(longitude, latitude, get_address(longitude, latitude))
    
    prompt = (f"你指定你是超級行程規劃師，不管任何行程你都會為我完成規劃，現在有一個人在{get_address(longitude, latitude)}的位置，請找出他目前的縣市，隨便推薦一整天的遊玩行程")
    response = model.generate_content(prompt)
    bot.reply_to(message, response.text)

if __name__ == "__main__":
    
    @bot.message_handler(content_types=['location'])
    def _handle_location(message):
        handle_location(message, bot)
    bot.infinity_polling()