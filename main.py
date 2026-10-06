import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import BOT_TOKEN
import database as db
from handlers import router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(name)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("pxl_detailing_bot")

async def main():
    if not BOT_TOKEN or BOT_TOKEN == "ВАШ_ТОКЕН_ОТ_BOTFATHER":
        logger.error("ОШИБКА: Укажите токен бота в файле .env (BOT_TOKEN=...)!")
        print("\n" + "="*60)
        print("❌ ОШИБКА: Откройте файл .env и вставьте BOT_TOKEN от @BotFather!")
        print("="*60 + "\n")
        return

    logger.info("Инициализация базы данных SQLite...")
    await db.init_db()

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)

    logger.info("Бот APEX Detailing Showroom успешно запущен! Нажмите Ctrl+C для остановки.")
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Бот остановлен.")
