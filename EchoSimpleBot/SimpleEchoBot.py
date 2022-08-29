from aiogram import Bot, Dispatcher, executor
import asyncio
from config import BOT_TOKEN

loop = asyncio.get_event_loop()

bot = Bot(BOT_TOKEN, parse_mode='HTML')  # Создание бота, выбор парсера

dp = Dispatcher(bot=bot, loop=loop)    # создание объекта обработчика. (Обрабатывает и доставляет данные)


if __name__ == '__main__':
    from handlers import dp, send_to_admin
    executor.start_polling(dp, on_startup=send_to_admin)            # Встроенная функция, делает запросы get_updates и доставляет сообщения