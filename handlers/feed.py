from aiogram import types
from storage import db
from services.pig_service import feed_pig

async def feed_handler(message: types.Message):
    user_id = message.from_user.id
    pig = db.get_pig(user_id)
    if not pig:
        await message.answer("Ти ще не маєш хряка! Використай /start")
        return

    feed_pig(pig)
    db.save_pig(pig)
    await message.answer(f"Твій хряк погодуваний! Нова вага: {pig.weight} кг, сила: {pig.strength}.")
    