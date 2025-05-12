from aiogram import types
from storage import supabase_storage as db
from utils.pig_helpers import ensure_pig_exists

async def name_handler(message: types.Message):
    user_id = message.from_user.id
    text = message.text

    parts = text.split(maxsplit=1)
    if len(parts) < 2:
        await message.answer("Введи ім'я через пробіл: /name [ім'я]")
        return

    new_name = parts[1].strip()

    if len(new_name) > 10:
        await message.answer("Ім'я не може бути довшим за 10 символів.")
        return

    pig = await ensure_pig_exists(message, user_id)
    if not pig:
        return

    all_pigs = db.get_all_pigs()
    for other_pig in all_pigs:
        if other_pig.name.lower() == new_name.lower() and other_pig.user_id != user_id:
            await message.answer("Таке ім’я вже зайняте іншим хряком! Спробуй інше 🐷")
            return

    pig.name = new_name
    db.save_pig(pig)
    await message.answer(f"Тепер твого хряка звуть {pig.name}!")
