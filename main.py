import asyncio
from aiogram import Bot, Dispatcher
from bot import setup_handlers
from storage import db
from dotenv import load_dotenv
import os

async def main():
    load_dotenv()
    db.load_db()

    bot = Bot(token=os.getenv("TELEGRAM_TOKEN"))
    dp = Dispatcher()

    router = setup_handlers()
    dp.include_router(router)

    print("🐷 Бот 'Свинопас' активний і слухає команди!")

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
