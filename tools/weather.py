import requests
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import telegram_token as TOKEN

if __name__ == '__main__':
    bot = telebot.TeleBot(TOKEN)

county_sitenames = {}
site_data = {}
weather_data = {}

def update_data():
    global county_sitenames, site_data, weather_data
    url = "https://data.moenv.gov.tw/api/v2/aqx_p_432?api_key=e8dd42e6-9b8b-43f8-991e-b3dee723a52d&limit=1000&sort=ImportDate%20desc&format=JSON"
    response = requests.get(url)
    data = response.json()

    url_2 = "https://opendata.cwa.gov.tw/fileapi/v1/opendataapi/F-C0032-001?Authorization=rdec-key-123-45678-011121314&format=JSON"
    response_w = requests.get(url_2)
    weather_data = response_w.json()

    for record in data['records']:
        county = record['county']
        sitename = record['sitename']
        if county not in county_sitenames:
            county_sitenames[county] = set()
        county_sitenames[county].add(sitename)
        site_data[sitename] = record

def create_county_keyboard():
    markup = InlineKeyboardMarkup(row_width=3)
    buttons = [InlineKeyboardButton(county, callback_data=f"county_{county}") for county in county_sitenames]
    markup.add(*buttons)
    return markup

def create_sitename_keyboard(county):
    markup = InlineKeyboardMarkup(row_width=3)
    buttons = [InlineKeyboardButton(sitename, callback_data=f"sitename_{sitename}") for sitename in county_sitenames[county]]
    markup.add(*buttons)
    return markup


# @bot.message_handler(commands=['weather'])
def weather(message, bot):
    update_data()
    markup = create_county_keyboard()
    bot.send_message(message.chat.id, "請選擇縣市：", reply_markup=markup)

# @bot.callback_query_handler(func=lambda call: call.data.startswith('county_') or call.data.startswith('sitename_'))
def callback_query(call, bot):
    if call.data.startswith('county_'):
        county = call.data.split('_')[1]
        markup = create_sitename_keyboard(county)
        bot.send_message(call.message.chat.id, f"請選擇{county}的測站：", reply_markup=markup)

    elif call.data.startswith('sitename_'):
        sitename = call.data.split('_')[1]
        data = site_data[sitename]

        for location in weather_data['cwaopendata']['dataset']['location']:
            if location['locationName'] == data['county']:
                weather_info = location
                break

        if weather_info:
            wx = next((item for item in weather_info['weatherElement'] if item['elementName'] == 'Wx'), None)
            pop = next((item for item in weather_info['weatherElement'] if item['elementName'] == 'PoP'), None)

            if wx and pop:
                weather_message = (
                    f"天氣: {wx['time'][0]['parameter']['parameterName']}\n"
                    f"降雨機率: {pop['time'][0]['parameter']['parameterName']}%"
                )
            else:
                weather_message = "無法獲取天氣資訊。"
        else:
            weather_message = "無法獲取天氣資訊。"
        
        message = (
            f"測站: {data['sitename']}\n"
            f"縣市: {data['county']}\n"
            f"{weather_message}\n"
            f"AQI: {data['aqi']}\n"
            f"狀態: {data['status']}\n"
            f"PM2.5: {data['pm2.5']}\n"
            f"PM10: {data['pm10']}\n"
            f"SO2: {data['so2']}\n"
            f"CO: {data['co']}\n"
            f"O3: {data['o3']}\n"
            f"NO2: {data['no2']}\n"
            f"風速: {data['wind_speed']}\n"
            f"風向: {data['wind_direc']}\n"
            f"發布時間: {data['publishtime']}"
        )
        bot.send_message(call.message.chat.id, message)

if __name__ == '__main__':
    @bot.message_handler(commands=['weather'])
    def _weather(message):
        weather(message, bot)
    @bot.callback_query_handler(func=lambda call: call.data.startswith('county_') or call.data.startswith('sitename_'))
    def _callback_query(call):
        callback_query(call, bot)
    bot.polling()
