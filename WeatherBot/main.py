import requests
from config import WEATHER_API_KEY
from pprint import pprint
from emoji import emojize
from datetime import datetime


def get_weather(city, token):

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
        req = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={token}&units=metric")
        data = req.json()
        pprint(data)

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
        print(f"*** {datetime.now().strftime('%Y-%m-%d %H:%M')} ***\n"
              f"Погода в городе {city}:\nТемпература: {cur_weather}C° {wd}\n"
              f"Влажность: {humidity}%\n"
              f"Давление: {pressure} мм.рт.ст\nСкорость ветра: {wind} м.с\n"
              f"Восход солнца: {sunrise_timestamp}\n"
              f"Заход солнца: {sunset_timestamp}\n"
              f"Продолжительность светового дня: {length_of_the_day}\n"
              f"Хорошего дня!"
              )




    except Exception as ex:
        print(ex)
        print("Название города введено не в верном формате. Проверьте название города.\n"
              "*** Название города должно быть введено латинскими буквами ***")


def main():
    city = input("Введите город:\n")
    get_weather(city=city, token=WEATHER_API_KEY)


if __name__ == '__main__':
    main()
