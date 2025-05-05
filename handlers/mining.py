from aiogram import types
from datetime import datetime, timedelta
import random
from storage import db

def can_mine(last_time_str: str) -> bool:
    if not last_time_str:
        return True
    last_time = datetime.strptime(last_time_str, "%Y-%m-%d %H:%M:%S")
    return datetime.now() - last_time > timedelta(minutes=0.1)

async def mining_handler(message: types.Message):
    user_id = message.from_user.id
    pig = db.get_pig(user_id)

    if not pig:
        await message.answer("Ти ще не маєш хряка! Використай /start")
        return

    if not can_mine(pig.last_mining_time):
        await message.answer("⛏️ Хряк ще втомлений після останнього копання. Спробуй пізніше!")
        return

    # Сценарії печер
    caves = [
        {"text": "Печера A: Хряк знайшов 10 золота!", "gold": 10},
        {"text": "Печера B: Нічого не знайшов...", "gold": 0},
        {"text": "Печера C: Хряк впав і втратив 10 ❤️!", "gold": 0, "damage": 10},
    ]
    result = random.choice(caves)
    text = result["text"]

    pig.gold += result.get("gold", 0)

    if "damage" in result:
        pig.health = max(1, pig.health - result["damage"])
        weight_loss = random.randint(10, 30)
        pig.weight = max(1, pig.weight - weight_loss)
        text += f"\n💥 Він також схуд на {weight_loss} кг!"

    pig.last_mining_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    db.save_pig(pig)

    await message.answer(text)

