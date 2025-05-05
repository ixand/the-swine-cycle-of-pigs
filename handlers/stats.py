from aiogram import types
from storage import db
from services.pig_service import get_rank

async def stats_handler(message: types.Message):
    user_id = message.from_user.id
    pig = db.get_pig(user_id)

    if not pig:
        await message.answer("Ти ще не маєш хряка! Використай /start")
        return

    rank = get_rank(pig)

    await message.answer(
        f"🐷 Ім'я: {pig.name}\n"
        f"🏅 Ранг: {rank}\n"
        f"📈 Рівень: {pig.level}\n"
        f"✨ Досвід: {pig.xp} XP\n"
        f"⚔️ Сила: {pig.strength}\n"
        f"🧠 Розум: {pig.mind}\n"
        f"❤️ Здоров'я: {pig.health}\n"
        f"🪙 Золото: {pig.gold}\n"
        f"⚖️ Вага: {pig.weight} кг"
    )
