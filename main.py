import asyncio
from aiogram import Bot, Dispatcher
from bot import setup_handlers
from storage import db
from dotenv import load_dotenv
import os
from aiohttp import web
import threading

async def main():
    load_dotenv()
    db.load_db()

    bot = Bot(token=os.getenv("TELEGRAM_TOKEN"))
    dp = Dispatcher()

    router = setup_handlers()
    dp.include_router(router)

    print("🐷 Бот 'Свинопас' активний і слухає команди!")

    await dp.start_polling(bot)

async def health(request):
    return web.Response(text="OK")

def start_web_server():
    app = web.Application()
    app.router.add_get("/health", health)
    web.run_app(app, port=8080)  # Railway слухає порт 8080


if __name__ == "__main__":
    threading.Thread(target=start_web_server, daemon=True).start()
    asyncio.run(main())
