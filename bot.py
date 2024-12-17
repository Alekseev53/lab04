import logging
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import TELEGRAM_BOT_TOKEN
from handlers import register_handlers

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=TELEGRAM_BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Регистрация хэндлеров
register_handlers(dp)

# Запуск бота
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
