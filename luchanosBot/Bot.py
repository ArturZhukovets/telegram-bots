import telebot
import pic_create
from config import BOT_TOKEN

bot = telebot.TeleBot(token=BOT_TOKEN, parse_mode="html")

@bot.message_handler(commands=['start', 'run', 'старт'])
def get_start(message):
    bot.send_message(chat_id=message.chat.id, text='Привет, я создан для того, чтобы генерировать случайную мем-картинку с твоим текстом,\n'
                                                   'но пока я могу только написать текст на рандомной картинке, через какое-то время мой функционал расширится!')
    bot.send_message(message.chat.id, text='Введи текст, который ты хочешь, чтобы я отобразил на пикче! С меня всё остальное!')

@bot.message_handler(content_types=['text'])
def generate_picture(message):
    try:
        if len(message.text) < 15:
            image_to_send = pic_create.create_image(message.text, 'red')
            bot.send_photo(message.chat.id, photo=image_to_send)
        else:
            bot.reply_to(message, text="Твой текст слишком длинный, не могу всё уместить, давай чуть меньше символов")
    except Exception as ex:
        bot.send_message(message.chat.id, f"{ex}Не вышло")

if __name__ == '__main__':
    bot.polling()