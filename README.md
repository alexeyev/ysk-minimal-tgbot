# ysk-minimal-tgbot
Based on earlier experience and Telegram / YSK docs

## Preparing secret keys
Create a file `config.ini` with the following contents:
```editorconfig
[telegram]
key=your_telegram_bot_key

[yandex]
id=your_yandex_cloud_service_api_id
key=your_yandex_cloud_service_api_key
```
I suggest that you do not commit it.

### Telegram
Ask @BotFather for a new bot and all the corresponding keys and stuff. Then write a secret key into `config.ini`
as a `[teleram].key` thing.

### Yandex
Get an API key for a Service at YandexCloud. You will be provided with your id and a key; this is the last time
you see your key, do not forget to copy and save it somewhere. Including `config.ini`.

## And we're good to go

```
python bot.py
```

## License
This is Beerware, so worry not.