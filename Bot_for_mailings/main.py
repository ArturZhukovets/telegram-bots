from uuid import uuid4

import bot_request
import telebot
from config import BOT_TOKEN
from telebot.types import Message
from telebot import types
from conversation_to_json import open_storage, add_to_storage, password_to_storage, add_review

import sqlite_worker

ADMIN_CHAT_ID = "489007270"
PATH_TO_STORAGE = './json_data.json'


bot = telebot.TeleBot(BOT_TOKEN, parse_mode='html')





@bot.message_handler(commands=['start', 'run', 'старт'])
def record_data(message: Message):
    """Генерация пользователя и возможность сгенерировать пароль при желании пользователя.
    Также если пользователь уже зарегистрирован, но у него нет пароля, есть возможность создать его(ветка else)"""
    data_from_json = open_storage(PATH_TO_STORAGE)

    # into JSON storage
    if add_to_storage(PATH_TO_STORAGE, message, data_from_json=data_from_json):
        # into sqlite
        sqlite_worker.add_user(message.from_user.id, message.from_user.username, user_firstname=message.from_user.first_name)
        bot.send_message(chat_id=message.chat.id, text='Добро пожаловать в банду!')
        # creating buttons

        reply_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        yes_button = types.KeyboardButton(text='Да')
        no_button = types.KeyboardButton(text='Нет')

        reply_markup.add(yes_button, no_button)
        msg = bot.send_message(chat_id=message.chat.id, text='Ты желаешь создать свой уникальный пароль для входа?', reply_markup=reply_markup)
        bot.register_next_step_handler(msg, confirm_generation)

    else:
        bot.send_message(message.chat.id, 'Такой айди уже есть')
        reply_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        yes_button = types.KeyboardButton(text='Да')
        no_button = types.KeyboardButton(text='Нет')
        reply_markup.add(yes_button, no_button)

        repeated_generation = bot.send_message(message.chat.id, text='Желаешь создать пароль?', reply_markup=reply_markup)
        bot.register_next_step_handler(repeated_generation, confirm_generation)


def confirm_generation(message: Message):
    upload_data = open_storage(PATH_TO_STORAGE)  # loading data from json storage
    str_user_id = str(message.from_user.id)
    if 'password' in upload_data[str_user_id].keys():
        bot.send_message(message.chat.id, text=f"Твой пароль уже есть в базе: <strong>{upload_data[str_user_id]['password']}</strong>")
    else:
        if message.text == "Да":
            # Создаётся пароль сразу здесь, чтобы отправить один и тот же password в оба хранилища
            password = str(uuid4()).split('-')[-1][:7]
            if password_to_storage(PATH_TO_STORAGE, message, password=password, data_from_json=upload_data): # generate a new password for user
                sqlite_worker.add_password(message.from_user.id, user_password=password)
                bot.send_message(message.chat.id, text=f'Пароль успешно сгенерирован! Ни в коем случае не потеряй!\n'
                                                       f'<strong>{password}</strong>')

        if message.text == "Нет":
            bot.send_message(message.chat.id, text=f"Ты зарегистрирован без пароля твой user_id в хранилище:{message.from_user.id}")


@bot.message_handler(commands=['say', 'say_standup_speach'])
def say_standup_speach(message):
    """Обработка команды say с последующей записью текста от пользователя в хранилище."""

    bot.reply_to(message, text="Привет, напиши мне какие трудности во время пользования сайтом у тебя возникли.\n"
                               "Я обработаю полученную информацию и отправлю тебе ответ, когда буду готов.")

    # регистрируем следующий шаг ОТ ЭТОГО пользователя и ждём его
    bot.register_next_step_handler(message, callback=handle_standup_speach)



def handle_standup_speach(message:Message):
    data_from_json = open_storage(PATH_TO_STORAGE)

    if add_review(PATH_TO_STORAGE, message, data_from_json):
        sqlite_worker.add_feedback(message.from_user.id, feedback=message.text)
        bot.reply_to(message, text="Спасибо за отзыв. Я постараюсь найти решение твоей проблемы и напишу тебе как только разберусь!")
    else:
        bot.reply_to(message, text="Что-то пошло не так и мне не удалось записать твою проблему :( ")



while True:
    try:
        if __name__ == '__main__':
            bot.polling()
    except Exception as err:
        """Примитивное логирование ошибок, посредством отлавливания и отправки сообщения об ошибке админу"""
        error_type = bot_request.bot_send_message(chat_id=ADMIN_CHAT_ID, text=err) # отправляем запрос с сообщением ошибки и сохраняем ответ в переменной.
        from_user_id = error_type['result']['chat']['id']
        from_user_name = error_type['result']['chat']['first_name']
        print(error_type)
        bot.send_message(ADMIN_CHAT_ID, text=f"{from_user_id} - {from_user_name}")
