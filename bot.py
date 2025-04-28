from aiogram import Router, F
from aiogram.filters import Command
from handlers import start, feed, name, stats, fight

router = Router()

def setup_handlers():
    router.message.register(start.start_handler, Command("start"))
    router.message.register(feed.feed_handler, Command("feed"))
    router.message.register(name.name_handler, Command("name"))
    router.message.register(stats.stats_handler, Command("stats"))
    router.message.register(fight.fight_handler, Command("fight"))
    return router
