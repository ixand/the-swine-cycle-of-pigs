from aiogram import types
from storage import db
from services.pig_service import attack, check_level_up, get_rank, handle_death
from utils.pig_helpers import ensure_pig_exists
from utils.constants import ATTACK_LIMIT_PER_DAY
from datetime import datetime
import random

async def attack_handler(message: types.Message):
    user_id = message.from_user.id
    pig1 = await ensure_pig_exists(message, user_id)
    if not pig1:
        return

    if not message.reply_to_message:
        await message.answer("Щоб битися, відповідай на повідомлення іншого гравця командою /attack.")
        return

    opponent_id = message.reply_to_message.from_user.id
    if opponent_id == user_id:
        await message.answer("Не можна битися із самим собою! 🤦‍♂️")
        return

    pig2 = db.get_pig(opponent_id)
    if not pig2:
        await message.answer("У опонента немає хряка!")
        return

    today = datetime.now().strftime("%Y-%m-%d")
    if pig1.last_fight_date != today:
        pig1.fights_today = 0
        pig1.last_fight_date = today

    if pig1.fights_today >= ATTACK_LIMIT_PER_DAY:
        await message.answer("Ти сьогодні вже провів 3 бої! Відпочивай. 🐖")
        return

    winner = attack(pig1, pig2)
    winner.xp += 10 + random.randint(1, 9)
    pig1.fights_today += 1

    loser = pig2 if winner.user_id == pig1.user_id else pig1
    health_loss = 10 + random.randint(1, 9)
    loser.health = max(0, loser.health - health_loss)

    text_death = handle_death(loser)
    db.save_pig(pig1)
    db.save_pig(pig2)

    if winner.user_id == user_id:
        text = f"🎉 Твій хряк {pig1.name} переміг {pig2.name} у нечесному бою!"
    else:
        text = f"😢 Твого хряка {pig1.name} переміг {pig2.name}..."

    await message.answer(text)
    await message.answer(text_death or f"{loser.name} втратив {health_loss} ❤️.")

    level_ups, level_text = check_level_up(winner)
    if level_ups > 0:
        if winner.level in (5, 10, 20):
            level_text += f"\n🎖️ Вітаємо! Твій хряк досяг рангу: {get_rank(winner)}!"
        db.save_pig(winner)
        await message.answer(level_text)