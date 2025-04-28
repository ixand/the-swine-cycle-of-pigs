from aiogram import types
from storage import db

async def stats_handler(message: types.Message):
    user_id = message.from_user.id
    pig = db.get_pig(user_id)
    if not pig:
        await message.answer("Ти ще не маєш хряка! Використай /start")
        return

    await message.answer(
        f"Ім'я: {pig.name}\n"
        f"Вага: {pig.weight} кг\n"
        f"Сила: {pig.strength}\n"
        f"Здоров'я: {pig.health}\n"
        f"Рівень: {pig.level}\n"
        f"Досвід: {pig.xp}"
    )
