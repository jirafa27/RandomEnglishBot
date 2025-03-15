import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from bot.config import TELEGRAM_BOT_TOKEN
from bot.handlers import router

logging.basicConfig(level=logging.INFO)


# Функция для подготовки окружения
def before_startup():
    os.makedirs("voices", exist_ok=True)  # Создаёт папку, если её нет
    logging.info("Папка voices готова для хранения файлов.")


async def main():
    before_startup()

    bot = None

    try:
        bot = Bot(
            token=TELEGRAM_BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML")
        )
        dp = Dispatcher()
        dp.include_router(router)
        logging.info("Бот запущен и ожидает сообщения...")

        await dp.start_polling(bot)

    except asyncio.CancelledError:
        logging.warning("Бот остановлен вручную (Ctrl+C)")

    except Exception as e:
        logging.error(f"Ошибка при запуске бота: {e}")

    finally:
        if bot:
            await bot.session.close()
            logging.info("Сессия бота закрыта")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Бот завершил работу")
