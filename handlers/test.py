from aiogram import types
from aiogram.filters import CommandObject
from services.pig_service import (
    handle_death,
    check_level_up,
    check_level_down,
    is_valid_change,
    exceeds_max_int,
    MAX_INT32
)
from storage import supabase_storage as db
from utils.pig_helpers import ensure_pig_exists

async def add_handler(message: types.Message, command: CommandObject):
    user_id = message.from_user.id
    pig = await ensure_pig_exists(message, user_id)
    if not pig:
        return

    args = command.args
    if not args:
        await message.answer("⚠️ Приклад: /add xp 100")
        return

    parts = args.split()
    if len(parts) < 2:
        await message.answer("⚠️ Використай: /add [тип] [значення]")
        return

    field = parts[0].lower()

    try:
        amount = int(parts[1])
    except ValueError:
        await message.answer("❌ Значення має бути числом (навіть від'ємним).")
        return

    updated = True
    msg = ""

    # === XP ===
    if field == "xp":
        if exceeds_max_int("xp", pig.xp, amount):
            await message.answer(f"❌ Неможливо мати XP більше ніж {MAX_INT32}.")
            return
        pig.xp += amount
        msg = f"✨ Змінено XP на {amount}\n"
        msg += check_level_down(pig)
        level_ups, rank_msg = check_level_up(pig)
        if level_ups:
            msg += f"\n🎉 {rank_msg or 'Хряк отримав бонуси за нові рівні!'}"

    # === Level ===
    elif field == "lvl":
        if not is_valid_change("level", pig.level, amount):
            msg = f"❌ Рівень не може бути нижчим за 1.\n"
            updated = False
        elif exceeds_max_int("level", pig.level, amount):
            msg = f"❌ Неможливо мати рівень більше ніж {MAX_INT32}.\n"
            updated = False
        else:
            pig.level += amount
            msg = f"⬆️ Змінено рівень на {amount}\n"
            level_ups, rank_msg = check_level_up(pig)
            if level_ups:
                msg += f"\n🎉 {rank_msg or 'Хряк отримав бонуси за нові рівні!'}"

    # === Strength ===
    elif field == "str":
        if not is_valid_change("strength", pig.strength, amount):
            msg = f"❌ Неможливо знизити силу нижче 1 (зараз: {pig.strength})"
            updated = False
        elif exceeds_max_int("strength", pig.strength, amount):
            msg = f"❌ Сила не може перевищувати {MAX_INT32}."
            updated = False
        else:
            pig.strength += amount
            msg = f"⚔️ {'Зменшено' if amount < 0 else 'Додано'} {abs(amount)} сили"

    # === Mind ===
    elif field == "min":
        if not is_valid_change("mind", pig.mind, amount):
            msg = f"❌ Неможливо знизити розум нижче 1 (зараз: {pig.mind})"
            updated = False
        elif exceeds_max_int("mind", pig.mind, amount):
            msg = f"❌ Розум не може перевищувати {MAX_INT32}."
            updated = False
        else:
            pig.mind += amount
            msg = f"🧠 {'Зменшено' if amount < 0 else 'Додано'} {abs(amount)} розуму"

    # === Gold ===
    elif field == "gol":
        if not is_valid_change("gold", pig.gold, amount):
            msg = f"❌ Неможливо мати менше 0 золота (зараз: {pig.gold})"
            updated = False
        elif exceeds_max_int("gold", pig.gold, amount):
            msg = f"❌ Золото не може перевищувати {MAX_INT32}."
            updated = False
        else:
            pig.gold += amount
            msg = f"🪙 {'Віднято' if amount < 0 else 'Додано'} {abs(amount)} золота"

    # === HP ===
    elif field == "hp":
        if exceeds_max_int("health", pig.health, amount):
            msg = f"❌ Здоров’я не може перевищувати {MAX_INT32}."
            updated = False
        else:
            pig.health += amount
            msg = f"❤️ Додано {amount} здоров'я"

    # === Max HP ===
    elif field == "mhp":
        if exceeds_max_int("max_health", pig.max_health, amount):
            msg = f"❌ Макс. здоров’я не може перевищувати {MAX_INT32}."
            updated = False
        else:
            pig.max_health += amount
            msg = f"❤️‍🩹 Додано {amount} до максимального здоров'я"

    # === Weight ===
    elif field == "mas":
        if exceeds_max_int("weight", pig.weight, amount):
            msg = f"❌ Вага не може перевищувати {MAX_INT32}."
            updated = False
        else:
            pig.weight += amount
            msg = f"⚖️ Додано {amount} кг ваги"

    # === Reset timers ===
    elif field == "pos":
        pig.last_feed_time = ""
        pig.last_fight_date = ""
        pig.last_quest_time = ""
        pig.last_mining_time = ""
        msg = "♻️ Всі позиційні таймери скинуто"

    else:
        updated = False
        msg = f"❌ Невідома властивість: {field}"

    # === Apply changes ===
    if updated:
        death_msg = handle_death(pig)
        db.save_pig(pig)
        if death_msg:
            msg += f"\n{death_msg}"

    await message.answer(msg)