from aiogram import Router, F
from aiogram.filters import Command
from handlers import start, feed, name, stats, fight, leaderboard, attack, help

router = Router()

def setup_handlers():
    router.message.register(start.start_handler, Command("start"))
    router.message.register(feed.feed_handler, Command("feed"))
    router.message.register(name.name_handler, Command("name"))
    router.message.register(stats.stats_handler, Command("stats"))
    router.message.register(attack.attack_handler, Command("attack"))
    router.message(Command("leaderboard"))(leaderboard.leaderboard_handler)
    router.message(Command("fight"))(fight.sparring_request_handler)
    router.callback_query()(fight.sparring_accept_handler)  # Додаємо колбек на кнопки
    router.message(Command("help"))(help.help_handler)
    return router
