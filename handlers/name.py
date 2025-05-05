from aiogram import types
from storage import db

async def name_handler(message: types.Message):
    user_id = message.from_user.id
    text = message.text

    parts = text.split(maxsplit=1)
    if len(parts) < 2:
        await message.answer("Введи ім'я через пробіл: /name [ім'я]")
        return

    new_name = parts[1].strip()

    # Перевірка довжини
    if len(new_name) > 10:
        await message.answer("Ім'я не може бути довшим за 10 символів.")
        return

    # Перевірка наявності хряка
    pig = db.get_pig(user_id)
    if not pig:
        await message.answer("Ти ще не маєш хряка! Використай /start")
        return

    # Перевірка, чи ім'я вже зайняте іншим гравцем
    all_pigs = db.get_all_pigs()
    for other_pig in all_pigs:
        if other_pig.name.lower() == new_name.lower() and other_pig.user_id != user_id:
            await message.answer("Таке ім’я вже зайняте іншим хряком! Спробуй інше 🐷")
            return

    # Успішна зміна імені
    pig.name = new_name
    db.save_pig(pig)
    await message.answer(f"Тепер твого хряка звуть {pig.name}!")
