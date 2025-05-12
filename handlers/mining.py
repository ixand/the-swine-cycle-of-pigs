from aiogram import types
from datetime import datetime, timedelta
import random
from storage import supabase_storage as db
from utils.pig_helpers import ensure_pig_exists
from services.pig_service import handle_death
from utils.constants import MINING_COOLDOWN_MINUTES

def can_mine(last_time_str: str) -> bool:
    if not last_time_str:
        return True
    last_time = datetime.strptime(last_time_str, "%Y-%m-%d %H:%M:%S")
    return datetime.now() - last_time > timedelta(minutes=MINING_COOLDOWN_MINUTES)

async def mining_handler(message: types.Message):
    user_id = message.from_user.id
    pig = await ensure_pig_exists(message, user_id)
    if not pig:
        return

    if not can_mine(pig.last_mining_time):
        await message.answer("⛏️ Хряк ще втомлений після останнього копання. Спробуй пізніше!")
        return

    caves = [
        {"text": "Печера A: Хряк знайшов 10 золота!", "gold": 10},
        {"text": "Печера B: Нічого не знайшов...", "gold": 0},
        {"text": "Печера C: Хряк впав і втратив 10 ❤️!", "gold": 0, "damage": 10},
    ]
    result = random.choice(caves)
    text = result["text"]

    pig.gold += result.get("gold", 0)

    if "damage" in result:
        pig.health = max(0, pig.health - result["damage"])
        weight_loss = random.randint(1, 15)
        pig.weight -= weight_loss

        text += f"\n💥 Він також схуд на {weight_loss} кг!"

        # Перевірка смерті від виснаження
        if pig.weight < 1:
            pig.weight = 1  # технічно не нуль, але смерть буде викликана
            pig.health = 0
            text += "\n☠️ Хряк настільки виснажився, що знепритомнів!"
        
        # Обробка смерті
        death_message = handle_death(pig)
        if death_message:
            text += f"\n{death_message}"

    pig.last_mining_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    db.save_pig(pig)
    await message.answer(text)
