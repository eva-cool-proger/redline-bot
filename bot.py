import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.client.session.aiohttp import AiohttpSession

from config import BOT_TOKEN
from database.db import init_db
from handlers import start, navigation, errors

async def set_bot_commands(bot: Bot):
    """Создает системное меню команд (кнопка Menu слева от поля ввода)"""
    commands =[
        BotCommand(command="start", description="Перезапустить гид / Restart"),
        BotCommand(command="lang", description="Сменить язык / Change language"),
        BotCommand(command="help", description="Справка / Help"),
    ]
    await bot.set_my_commands(commands)

async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )
    
    await init_db()
    
    session = AiohttpSession(timeout=60)

    bot = Bot(token=BOT_TOKEN, session=session)
    dp = Dispatcher()
    
    dp.include_router(start.router)
    dp.include_router(navigation.router)
    dp.include_router(errors.router)
    
    await set_bot_commands(bot)
    
    logging.info("🚀 Бот успешно запущен!")
    await bot.delete_webhook(drop_pending_updates=True)
    
    try:
        await dp.start_polling(bot)
    finally:
        # Корректное закрытие сессии бота при выключении
        await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("🛑 Бот остановлен вручную.")