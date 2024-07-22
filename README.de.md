# SITCON-Camp-2024-Team5

[English](README.md) | [繁體中文](README.zh-TW.md) | Deutsch

## Was kann dieser Bot tun?

Dieser Bot wird dich sehr gut über deinen Tag informieren und dein Leben viel einfacher machen!
`/help` - Liste der Befehle abrufen  
`/weather` - Das Wetter einer Stadt abrufen  
`/set_calendar_link` [Link] - Gib dem Bot deinen Benutzernamen für deinen Google-Kalender  
`/calendar_today` - Die Ereignisse des heutigen Tages abrufen  
`/set_calendar_notify` [Zeit] - Die Zeit festlegen, zu der du über die Ereignisse des Tages benachrichtigt werden möchtest  
[Ort] - Sende deinen Standort und der Bot wird dir einen Tagesplan für den Ort in deiner Nähe mitteilen  
`/picture`[Satz] - Bilder für Morgen, Mittag und Abend abrufen  
`/color` - Die Farbe der Wörter im Bild ändern  

## Einrichtung

1. Installationspaket

   - Installation über pip

   ```bash
   pip install -r requirements.txt
   ```

   - Installation über poetry

   ```bash
   poetry install
   ```

2. Deine eigene Konfiguration ausfüllen

   - Kopiere die Datei `config_template.py` nach `config.py`
   - Fülle deinen Telegram-Bot-Token und den Geming-API-Schlüssel aus

## Ausführen

```bash
python main.py
```
