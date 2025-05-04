from aiogram import types
from storage import db
from services.pig_service import check_level_up, get_rank, attack
from datetime import datetime, timedelta
import random

async def attack_handler(message: types.Message):
    user_id = message.from_user.id
    pig1 = db.get_pig(user_id)

    if not pig1:
        await message.answer("Ти ще не маєш хряка! Використай /start")
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

    # Лімітуємо бої на день
    today = datetime.now().strftime("%Y-%m-%d")
    if pig1.last_fight_date != today:
        pig1.fights_today = 0
        pig1.last_fight_date = today

    if pig1.fights_today >= 3:
        await message.answer("Ти сьогодні вже провів 3 бої! Відпочивай. 🐖")
        return

    # Атака
    winner = attack(pig1, pig2)
    winner.xp += 10 + random.randint(1,9)
    pig1.fights_today += 1

    # Якщо програв — мінус здоров'я
    loser = pig2 if winner.user_id == pig1.user_id else pig1
    health_loss = 10 + random.randint(1, 9)

    if loser.health <= 10 and health_loss >= 10:
        # Помирає — обнуляємо
        loser.level = 1
        loser.xp = 0
        loser.health = 100
        text_death = f"☠️ {loser.name} помер у бою і був відроджений на рівні 1!"
    
        
    else:
        # Просто втрачає здоров'я
        loser.health = max(1, loser.health - health_loss)
        text_death = f"{loser.name} втратив {health_loss} ❤️."

    db.save_pig(pig1)
    db.save_pig(pig2)

    # Формуємо текст
    if winner.user_id == user_id:
        text = f"🎉 Твій хряк {pig1.name} переміг {pig2.name} у нечесному бою!"
    else:
        text = f"😢 Твого хряка {pig1.name} переміг {pig2.name}..."

    
    old_level = winner.level  # зберігаємо попередній рівень
    level_ups = check_level_up(winner)

    if level_ups > 0:
        level_text = (
        f"🏅 Твій хряк підняв рівень на {level_ups}!\n"
        f"➕ Сила +{level_ups}, Здоров'я +{level_ups * 10}"
    )

    new_level = old_level + level_ups
    if new_level in (5, 10, 20):
        new_rank = get_rank(winner)
        level_text += f"\n🎖️ Вітаємо! Твій хряк досяг рангу: {new_rank}!"

    await message.answer(level_text)  # окреме повідомлення
