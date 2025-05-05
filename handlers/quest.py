from aiogram import types
from storage import db
from services.quest_service import apply_quest
from datetime import datetime

async def quest_handler(message: types.Message):
    user_id = message.from_user.id
    pig = db.get_pig(user_id)

    if not pig:
        await message.answer("Ти ще не маєш хряка! Використай /start")
        return

    today = datetime.now().strftime("%Y-%m-%d")
    if getattr(pig, "last_quest_date", "") == today:
        await message.answer("Сьогодні ти вже виконав квест. Повертайся завтра!")
        return

    quest = apply_quest(pig)
    db.save_pig(pig)

    text = f"🎯 Квест: *{quest['title']}*\n\n{quest['description']}\n\n🎁 Нагорода: " + \
        ", ".join([f"+{v} {k}" for k, v in quest["effects"].items()])
    
    await message.answer(text, parse_mode="Markdown")
