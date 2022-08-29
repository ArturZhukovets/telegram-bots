from config import API_KEY, BOT_TOKEN

import telebot
from telebot.types import Message
from telebot import types

import get_picture

ADMIN = "489007270"

QUERY = ""
NUMBER_OF_PICTURES = "1"

bot = telebot.TeleBot(BOT_TOKEN, parse_mode='html')


@bot.message_handler(commands=['start'])
def start(message:Message):
    reply_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    get_image_button = types.KeyboardButton("Get image!")
    reply_markup.add(get_image_button)

    start_message = bot.send_message(message.chat.id, text="Hello, what would you like to do?\n"
                                                           "(Choose any option below)", reply_markup=reply_markup)
    bot.register_next_step_handler(start_message, get_query)


def get_query(message: Message):
    msg = bot.send_message(message.chat.id, text="Please enter a search term for the picture you want to get.")
    bot.register_next_step_handler(msg, get_image)


def get_image(message:Message):
    global QUERY
    QUERY = message.text

    bot.send_message(message.chat.id, text="Excellent! Wait few seconds, please.")
    picture = get_picture.get_picture(QUERY, NUMBER_OF_PICTURES)
    bot.send_photo(chat_id=message.chat.id, photo=picture, caption=QUERY)


while True:
    try:
        bot.polling()
    except Exception as ex:
        bot.send_message(chat_id=ADMIN, text=f"{ex}")






