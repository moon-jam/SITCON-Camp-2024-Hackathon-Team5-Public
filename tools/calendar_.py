import os
import json
import requests
from icalendar import Calendar
import telebot
import time
from datetime import datetime
from config import telegram_token as TOKEN

if __name__ == "__main__":
    bot=telebot.TeleBot(TOKEN)

# 從 URL 下載 ICS 文件
def download_ics(url, download_path):
    response = requests.get(url)
    response.raise_for_status()
    with open(download_path, 'wb') as file:
        file.write(response.content)

# 解析 ICS 文件
def parse_ics(file_path):
    with open(file_path, 'rb') as file:
        cal = Calendar.from_ical(file.read())
    
    events = []
    for component in cal.walk():
        if component.name == "VEVENT":
            event = {
                "summary": str(component.get('summary')),
                "dtstart": component.decoded('dtstart').isoformat(),
                "dtend": component.decoded('dtend').isoformat() if component.get('dtend') else None,
                "description": str(component.get('description')),
                "location": str(component.get('location'))
            }
            events.append(event)
    return events

# 將資料寫入 JSON 文件
def write_to_json(data, json_file_path):
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

# update_calendar
def update_calendar(ics_url, download_path, json_file_path):
    download_ics(ics_url, download_path)
    events = parse_ics(download_path)
    write_to_json(events, json_file_path)
    os.remove(download_path)
    print(f"ICS 文件已成功轉換為 JSON 文件，儲存在 {json_file_path} 並已刪除下載的 ICS 文件")   

# @bot.message_handler(commands=["set_calendar_link"])
def set_calendar_link(message, bot):
    ics_url = message.text[19:]
    # 读取JSON文件
    with open("./database/calendar_user_info.json", "r") as file:
        data = json.load(file)
    
    # 修改["time"]为time_string
    data["link"] = ics_url

    # 将修改后的数据写回JSON文件
    with open("./database/calendar_user_info.json", "w") as file:
        json.dump(data, file)
    
    with open("./database/calendar_user_info.json", "r") as file:
        data = json.load(file)
        
        ics_url = data["link"]
        notify_time = data["time"]
        
        if ics_url != "":
            print(f"已設定日曆連結: {ics_url}")
            try:
                # 更新日曆
                download_path = 'basic.ics'
                update_calendar(ics_url, download_path, './database/calendar.json')
            except Exception as e:
                print(f"更新日曆失敗: {e}")
    
    bot.send_message(message.chat.id, "你的日曆鏈結已設定完成")

    # download_path = 'basic.ics'
    # json_file_path = './database/calendar.json'
    # main(ics_url, download_path, json_file_path)
    # bot.reply_to(message,"你的日曆數據已匯入完成")

# @bot.message_handler(commands=["set_calendar_notify"])
def set_calendar_notify(message, bot):
    time=message.text[21:].split(":")
    time_string = f"{time[0]}{time[1]}"
    # 读取JSON文件
    with open("./database/calendar_user_info.json", "r") as file:
        data = json.load(file)
    
    # 修改["time"]为time_string
    data["time"] = time_string

    # 将修改后的数据写回JSON文件
    with open("./database/calendar_user_info.json", "w") as file:
        json.dump(data, file)
        
    bot.send_message(message.chat.id, "你的日曆通知時間已設定完成")

# @bot.message_handler(commands=["calendar_today"])
def today(message, bot):
    # handle_calendar()
    # today_list={}
    # start_time=[]
    output="這是你今天的行事曆\n"
    with open("./database/calendar.json","r") as file:
        import_calendar=json.load(file)
    for i in range(len(import_calendar)):
        # print(import_calendar[i])
        start_time=import_calendar[i]["dtstart"][:10]
        print(start_time, datetime.now().strftime("%Y-%m-%d"))
        if start_time==datetime.now().strftime("%Y-%m-%d"):
            # today_list.append(import_calendar[i])    
            output += f"{import_calendar[i]["dtstart"][11:16]}~{import_calendar[i]["dtend"][11:16]} {import_calendar[i]["summary"]}\n\n"
    bot.send_message(message.chat.id, output)

# @bot.message_handler(commands=["start"])
def start_thread(message, bot):
    # bot.send_message(message.chat.id,"請將日曆設為公開，並將下載ICS的連結回傳")
    # bot.reply_to(message,"start")
    while True:
        time.sleep(50)
        
        with open("./database/calendar_user_info.json", "r") as file:
            data = json.load(file)
            
            ics_url = data["link"]
            notify_time = data["time"]
            
            if ics_url != "":
                print(f"已設定日曆連結: {ics_url}")
                try:
                    # 更新日曆
                    download_path = 'basic.ics'
                    update_calendar(ics_url, download_path, './database/calendar.json')
                except Exception as e:
                    print(f"更新日曆失敗: {e}")
                
                if notify_time == "":
                    continue
                
                if datetime.now().strftime("%H%M")==notify_time:
                    print(datetime.now().strftime("%H%M"))
                    # 確認時間是否到達設定值
                    print(datetime.now().strftime("%H%M"))
                    today(message, bot)
                    print("hahahaha")
                    time.sleep(60)

import threading

def start(message, bot):
    t = threading.Thread(target=start_thread, args=(message, bot))
    t.start()

if __name__ == "__main__":
    @bot.message_handler(commands=["set_calendar_link"])
    def _set_calendar_link(message, bot):
        set_calendar_link(message, bot)

    @bot.message_handler(commands=["set_calendar_notify"])
    def _set_calendar_notify(message, bot):
        set_calendar_notify(message, bot)

    @bot.message_handler(commands=["calendar_today"])
    def _today(message, bot):
        today(message, bot)

    @bot.message_handler(commands=["start"])
    def _start(message, bot):
        start(message, bot)
    
    bot.polling(none_stop=True)