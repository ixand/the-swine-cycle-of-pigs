from aiogram import types
from storage import db

async def name_handler(message: types.Message):
    user_id = message.from_user.id
    text = message.text

    parts = text.split(maxsplit=1)

    if len(parts) < 2:
        await message.answer("Введи ім'я через пробіл: /name [ім'я]")
        return

    new_name = parts[1]

    pig = db.get_pig(user_id)
    if not pig:
        await message.answer("Ти ще не маєш хряка! Використай /start")
        return

    pig.name = new_name
    db.save_pig(pig)
    await message.answer(f"Тепер твого хряка звуть {pig.name}!")
