from aiogram import types
from storage import db
from services.pig_service import fight

async def fight_handler(message: types.Message):
    user_id = message.from_user.id
    pig1 = db.get_pig(user_id)
    if not pig1:
        await message.answer("Ти ще не маєш хряка! Використай /start")
        return

    if not message.reply_to_message:
        await message.answer("Щоб битися, відповідай на повідомлення іншого гравця командою /fight")
        return

    opponent_id = message.reply_to_message.from_user.id
    pig2 = db.get_pig(opponent_id)
    if not pig2:
        await message.answer("У опонента немає хряка!")
        return

    winner = fight(pig1, pig2)

    if winner.user_id == user_id:
        pig1.xp += 10
        db.save_pig(pig1)
        await message.answer(f"Твій хряк {pig1.name} переміг!")
    else:
        pig2.xp += 10
        db.save_pig(pig2)
        await message.answer(f"Твого хряка {pig1.name} побито!")
