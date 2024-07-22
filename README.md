# SITCON-Camp-2024-Hackathon-Team5

English | [繁體中文](README.zh-TW.md) | [Deutsch](README.de.md)

## What can this bot do?

This bot will inform you about your day very well and will make your life much easier!
`/help` - Get the list of commands  
`/weather` - Get the weather of a city  
`/set_calendar_link` [link] - Give the bot your username for your google calendar  
`/calendar_today` - Get the events of today  
`/set_calendar_notify` [time] - Set the time to notify you about the events of the day  
[location] - send your location, and the bot will tell you a today-schedule about the place near you  
`/picture`[sentence] - Get morning,noon and evening pictures  
`/color` - Change the word color in the picture "  

## Setup

1. Installation package

   - Install via pip

   ```bash
   pip install -r requirements.txt
   ```

   - Install via poetry

   ```bash
   poetry install
   ```

2. Fill in your own configuration

   - Copy the `config_template.py` file to `config.py`
   - Fill in your Telegram bot token ans Geming API key

## Run

```bash
python main.py
```
