import config
import telebot
import requests
from emoji import emojize
from pprint import pprint
from telebot import types
from datetime import datetime

bot = telebot.TeleBot(config.BOT_TOKEN)


@bot.message_handler(commands=['start', 'старт'])
def start_weather(message: types.Message):
    bot.reply_to(message, 'Приветствую! Я пока ничего не  особого не умею, но хоть чем-то к'
                          'полезным быть смогу.\n'
                          'В общем, напиши название любого города, желательно, правильно, и я дам тебе детальный прогноз погоды на сегодняшний день!')
    bot.send_message(chat_id=message.chat.id, text="Введи название города:")


@bot.message_handler()
def get_weather(message):
    unicode_to_emoji = {
        'Clear': f'Ясно \U00002600',
        'Thunderstorm': f'Гроза {emojize(":cloud_with_lightning_and_rain:")}',
        'Drizzle': f'Мелкий дождь \U00002614',
        'Rain': f'Дождь {emojize(":cloud with rain:")}',
        'Snow': f'Снег {emojize(":snowflake:")}',
        'Mist': f'Туман \U0001F32B',
        'Clouds': f'Облачно {emojize(":cloud:")}',

    }

    try:
        req = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={config.WEATHER_API_KEY}&units=metric")
        data = req.json()
        # pprint(data)
        weather_descr = data['weather'][0]['main']
        if weather_descr in unicode_to_emoji:
            wd = unicode_to_emoji[weather_descr]
        else:
            wd = "Лучше посмотри пойму в окно, ибо я не пойму что там :)"

        city = data['name']
        cur_weather = data['main']['temp']
        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
        wind = data['wind']['speed']
        sunrise_timestamp = datetime.fromtimestamp(data['sys']['sunrise'])
        sunset_timestamp = datetime.fromtimestamp(data['sys']['sunset'])
        length_of_the_day = sunset_timestamp - sunrise_timestamp
        bot.reply_to(message=message,
                     text=f"*** {datetime.now().strftime('%Y-%m-%d %H:%M')} ***\n"
                          f"Погода в городе {city}:\nТемпература: {cur_weather}C° {wd}\n"
                          f"Влажность: {humidity}%\n"
                          f"Давление: {pressure} мм.рт.ст\nСкорость ветра: {wind} м.с\n"
                          f"Восход солнца: {sunrise_timestamp}\n"
                          f"Заход солнца: {sunset_timestamp}\n"
                          f"Продолжительность светового дня: {length_of_the_day}\n"
                          f"Хорошего дня!"
                     )




    except:
        bot.reply_to(message,
                     "Название города введено не в верном формате. Проверьте название города.\n"
                     "Совет: Название города должно быть введено латинскими буквами.")


if __name__ == '__main__':
    bot.polling()
