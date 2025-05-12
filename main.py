import asyncio
from aiogram import Bot, Dispatcher
from bot import setup_handlers
from storage import supabase_storage as db
from dotenv import load_dotenv
from aiohttp import web
import os

async def health(request):
    return web.Response(text="OK")

async def start_web_server():
    app = web.Application()
    app.router.add_get("/health", health)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 8080)  # слухає на Railway
    await site.start()

async def main():
    load_dotenv()

    bot = Bot(token=os.getenv("TELEGRAM_TOKEN"))
    dp = Dispatcher()
    router = setup_handlers()
    dp.include_router(router)

    print("🐷 Бот 'Свинопас' активний і слухає команди!")

    # Паралельно стартує aiohttp сервер і polling
    await asyncio.gather(
        start_web_server(),
        dp.start_polling(bot),
    )

if __name__ == "__main__":
    asyncio.run(main())
