from config import BOT_TOKEN
from telebot import types
import telebot

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['info', 'get_info'])
def get_user_info(message):
    inline_buttons = types.InlineKeyboardMarkup()
    yes_button = types.InlineKeyboardButton(text="Да", callback_data="yes")
    no_button = types.InlineKeyboardButton(text="Нет", callback_data="no")
    button_to_information = types.InlineKeyboardButton(text="Узнать, что может этот бот (ничего)", callback_data='info')

    inline_buttons.add(yes_button, no_button, button_to_information)
    bot.send_message(message.chat.id, 'Привет, я Бениксоидиус!!!\n'
                                      'Ты хочешь узнать инфу про себя? Или просто хочешь ознакомится с моим функционалом?',
                     reply_markup=inline_buttons)  # Прикрепляю кнопки к этому сообщению

# markup = types.ReplyKeyboardMarkup()
# markup.row('a', 'v')
# markup.row('c', 'd', 'e')
# tb.send_message(chat_id, message, reply_markup=markup)
@bot.message_handler(commands=['reg', 'registration'])
def registration(message):
    """Появляется клава с двумя кнопками. При любом действии вызывается следующее событие,
     в котором описывается логика взаимодействия с кнопками"""
    reply_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, # resize_kb Кнопки становятся меньше по размеру
                                             one_time_keyboard=True)  # one_time_kb Клавиатура исчезает после первого использования
    button1_yes = types.KeyboardButton("Да")
    button2_net = types.KeyboardButton("Нет")



    reply_markup.row(button1_yes)
    reply_markup.row(button2_net)



    msg = bot.send_message(message.chat.id, "Желаешь оставить заявку?", reply_markup=reply_markup)
    bot.register_next_step_handler(msg, user_confirm)  # Регистрируем следующий шаг, затем переходим на функцию user_confirm


def user_confirm(message):
    """Вызывается сообщение В случае если ответ ДА, дальше опять регистрируем следующий шаг"""
    if message.text == 'Да':
        msg = bot.send_message(message.chat.id, text="Запиши свои данные: Имя, фамилия, год. В формате X X X\n"
                                                     "Например: Ахмед Шмелёв 1990")
        bot.register_next_step_handler(msg, user_registration)
    elif message.text == "Нет":
        bot.send_message(message.chat.id, text="Окей, обсыхай, бродяга")

    else:
        bot.send_message(message.chat.id, text='Зафиксировано неправильное событие, ты отправляешься на главную.\n'
                                               ' Если захочешь повторить, напиши команду /reg')


def user_registration(message):
    if len(message.text.split()) == 3 and all([i.isalpha() for i in message.text.split()[:2]]) and message.text.split()[-1].isdigit():
        bot.send_message(message.chat.id, text=f"Твои данные успешно сохранены. {message.text} ")
    else:
        bot.send_message(message.chat.id, text="Ты некорректно ввёл данные. Попробуй ещё раз. Сынок. ")


# Обработчик обратного запроса для команды info
@bot.callback_query_handler(func=lambda call: True)
def answer(call):
    bot.answer_callback_query(callback_query_id=call.id)  # необходимо для того, чтобы после нажатия на кнопку бот фиксировал событие и кнопка "отжималась"
    """Если yes, то создается ещё одна клавиатура ReplyKeyboardMarkup"""

    if call.data == 'yes':
        markup_reply_buttons = types.ReplyKeyboardMarkup(
            resize_keyboard=True, one_time_keyboard=True)  # resize для того, чтобы клаву кнопку сделать меньше
        item_id = types.KeyboardButton('Мой ID')  # В чат отправляется Мой ID
        item_username = types.KeyboardButton("Мой Username")  # В чат отправляется Мой Username

        markup_reply_buttons.add(item_id, item_username)  # добавляем кнопки в клаву ReplyKeyboardMarkup
        bot.send_message(call.message.chat.id, 'Выбери, что тебя интересует',
                         reply_markup=markup_reply_buttons)  # Прикрепляю клаву к этому сообщению

    elif call.data == "no":
        bot.send_message(call.message.chat.id, text="Окей, ну и не надо. Счастливо оставаться!")
    elif call.data == "info":
        bot.send_message(call.message.chat.id, text="Значит, я пока что могу только послать тебя в жопу, для этого ничего можешь не вводить и не нажимать.\n"
                                                    "Кроме того я могу зарегистрировать твои данные в своей БД (которая ещё не подключена).\n"
                                                    "Чтобы зарегистрироваться напиши команду /reg.")

    # bot.answer_callback_query(callback_query_id=call.id)  # необходимо для того, чтобы после нажатия на кнопку бот фиксировал событие и кнопка "отжималась"


@bot.message_handler(content_types=['text'])
def get_text_from_info(message):
    """Обработка по тексту, который приходит в обработчик из кнопки."""
    if message.text == 'Мой ID':
        bot.send_message(chat_id=message.chat.id, text=f"Твой ID: {message.from_user.id}")
        print(message.chat.id)

    elif message.text == 'Мой Username':
        bot.send_message(chat_id=message.chat.id, text=f"Твой Username: {message.from_user.username}")

if __name__ == '__main__':
    bot.polling()
