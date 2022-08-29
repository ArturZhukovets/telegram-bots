import requests
from datetime import datetime
import telebot
from auth_data import BOT_TOKEN


def get_data():
    req = requests.get(url='https://yobit.net/api/3/ticker/btc_usd')
    response = req.json()
    # print(response)
    sell_price = response['btc_usd']['sell']
    # print(f"{datetime.now().strftime('%Y-%m-%d %H:%M')}\nSell BTC price: {sell_price}")



def telegram_bot(token):
    bot = telebot.TeleBot(token=token)

    @bot.message_handler(commands=["start"])
    def start_massage(message):
        bot.send_message(message.chat.id, "Hello, friend! Write the 'price' to find out the coast of BTC(bitcoin).")


    @bot.message_handler(content_types=['text'])
    def send_text(message):
        if message.text.lower() == 'price':
            try:
                req = requests.get(url='https://yobit.net/api/3/ticker/btc_usd')
                response = req.json()
                sell_price = response['btc_usd']['sell']
                bot.send_message(message.chat.id,
                                 f"{datetime.now().strftime('%Y-%m-%d %H:%M')}\nSell BTC price: {sell_price}")
            except Exception as ex:
                print(ex)
                bot.send_message(message.chat.id, "Something was wrong...")

        else:
            bot.send_message(message.chat.id, "What? I can't understand this command, dude! Try again and check command name.")



    bot.polling()


if __name__ == '__main__':
    # get_data()
    telegram_bot(BOT_TOKEN)