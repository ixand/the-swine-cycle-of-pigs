from aiogram import types
from storage import db
from services.pig_service import fight as pig_fight, check_level_up, get_rank
from datetime import datetime, timedelta
import random

async def fight_handler(message: types.Message):
    user_id = message.from_user.id
    pig1 = db.get_pig(user_id)

    if not pig1:
        await message.answer("Ти ще не маєш хряка! Використай /start")
        return

    if not message.reply_to_message:
        await message.answer("Щоб битися, відповідай на повідомлення іншого гравця командою /fight.")
        return

    opponent_id = message.reply_to_message.from_user.id
    if opponent_id == user_id:
        await message.answer("Не можна битися із самим собою! 🤦‍♂️")
        return

    pig2 = db.get_pig(opponent_id)
    if not pig2:
        await message.answer("У опонента немає хряка!")
        return

    # Лімітуємо бої на день
    today = datetime.now().strftime("%Y-%m-%d")
    if pig1.last_fight_date != today:
        pig1.fights_today = 0
        pig1.last_fight_date = today

    if pig1.fights_today >= 3:
        await message.answer("Ти сьогодні вже провів 3 бої! Відпочивай. 🐖")
        return

    # Бій
    winner = pig_fight(pig1, pig2)

    winner.xp += 10
    level_ups = check_level_up(winner)

    # Якщо програв — мінус здоров'я
    loser = pig2 if winner.user_id == pig1.user_id else pig1
    health_loss = 10 + random.randint(1, 9)
    loser.health = max(1, loser.health - health_loss)  # Здоров'я не може бути менше 1

    pig1.fights_today += 1

    db.save_pig(pig1)
    db.save_pig(pig2)

    # Формуємо текст
    if winner.user_id == user_id:
        text = f"🎉 Твій хряк {pig1.name} переміг {pig2.name} у чесному бою!"
    else:
        text = f"😢 Твого хряка {pig1.name} переміг {pig2.name}..."

    if level_ups > 0:
        rank = get_rank(winner)
        text += f"\n🏅 Твій хряк підняв рівень на {level_ups}!\n➕ Сила +{level_ups}, Здоров'я +{level_ups * 10}\nНовий ранг: {rank}"

    text += f"\n\n{loser.name} втратив {health_loss} ❤️."

    await message.answer(text)
