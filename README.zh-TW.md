# SITCON-Camp-2024-Team5

[English](README.md) | 繁體中文 | [Deutsch](README.de.md)

## 這個機器人能做什麼？

這個機器人能很好地通知你每天的行程，讓你的生活更輕鬆！
`/help` - 獲取指令列表  
`/weather` - 獲取城市的天氣  
`/set_calendar_link` [連結] - 提供機器人你的 Google 日曆使用者名稱  
`/calendar_today` - 獲取今天的事件  
`/set_calendar_notify` [時間] - 設定通知你今天事件的時間  
[位置] - 發送你的位置，機器人會告訴你附近地區的今日行程  
`/picture` [句子] - 獲取早晨、中午和晚上的圖片 (句子是選填的，如果沒有填入會依照目前時間由Gemini自動生成句子)  
`/color` - 更改圖片中單詞的顏色  

## 設置

1. 安裝套件

   - 通過 pip 安裝

   ```bash
   pip install -r requirements.txt
   ```

   - 通過 poetry 安裝

   ```bash
   poetry install
   ```

2. 填寫你的配置

   - 將 `config_template.py` 文件複製為 `config.py`
   - 填寫你的 Telegram 機器人 token 和 Geming API 密鑰

## 運行

```bash
python main.py
```
