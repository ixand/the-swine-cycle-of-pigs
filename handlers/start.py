from aiogram import types
from storage import db
from services.pig_service import init_pig

async def start_handler(message: types.Message):
    user_id = message.from_user.id
    if db.get_pig(user_id):
        await message.answer("У тебе вже є хряк!")
    else:
        pig = init_pig(user_id)
        db.save_pig(pig)
        await message.answer("Створено нового хряка! Використай /name [ім'я] щоб назвати його.")

