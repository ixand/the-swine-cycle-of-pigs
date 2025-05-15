from aiogram import types
from aiogram.filters import CommandObject
from services.pig_service import handle_death
from storage import supabase_storage as db
from utils.pig_helpers import ensure_pig_exists
from services.pig_service import check_level_up, check_level_down, is_valid_change

async def add_handler(message: types.Message, command: CommandObject):
    user_id = message.from_user.id
    pig = await ensure_pig_exists(message, user_id)
    if not pig:
        return

    args = command.args
    if not args:
        await message.answer("⚠️ Приклад: /test xp 100\n")
        return

    parts = args.split()
    if len(parts) < 2:
        await message.answer("⚠️ Використай: /test [тип] [значення]\n")
        return

    field = parts[0].lower()

    try:
        amount = int(parts[1])
    except ValueError:
        await message.answer("❌ Значення має бути числом (навіть від'ємним).\n")
        return

    updated = True
    msg = ""

    if field == "xp":
        pig.xp += amount
        msg = f"✨ Змінено XP на {amount}\n"
        msg += check_level_down(pig)
        level_ups, rank_msg = check_level_up(pig)
        if level_ups:
            msg += f"\n🎉 {rank_msg or 'Хряк отримав бонуси за нові рівні!\n'}"

    elif field == "lvl":
        pig.level = max(1, pig.level + amount)
        msg = f"⬆️ Змінено рівень на {amount}\n"
        level_ups, rank_msg = check_level_up(pig)
        if level_ups:
            msg += f"\n🎉 {rank_msg or 'Хряк отримав бонуси за нові рівні!\n'}"

    elif field == "str":
        if not is_valid_change("strength", pig.strength, amount):
            msg = f"❌ Неможливо знизити силу нижче 1 (зараз: {pig.strength})\n"
            updated = False
        else:
            pig.strength += amount
            msg = f"⚔️ {'Зменшено' if amount < 0 else 'Додано'} {abs(amount)} сили\n"

    elif field == "min":
        if not is_valid_change("mind", pig.mind, amount):
            msg = f"❌ Неможливо знизити розум нижче 1 (зараз: {pig.mind})\n"
            updated = False
        else:
            pig.mind += amount
            msg = f"🧠 {'Зменшено' if amount < 0 else 'Додано'} {abs(amount)} розуму\n"

    elif field == "gol":
        if not is_valid_change("gold", pig.gold, amount):
            msg = f"❌ Неможливо мати менше 0 золота (зараз: {pig.gold})\n"
            updated = False
        else:
            pig.gold += amount
            msg = f"🪙 {'Віднято' if amount < 0 else 'Додано'} {abs(amount)} золота\n"

    elif field == "hp":
        pig.health += amount
        msg = f"❤️ Додано {amount} здоров'я\n"

    elif field == "mhp":
        pig.max_health += amount
        msg = f"❤️‍🩹 Додано {amount} до максимального здоров'я\n"

    elif field == "mas":
        pig.weight += amount
        msg = f"⚖️ Додано {amount} кг ваги\n"

    elif field == "pos":
        pig.last_feed_time = ""
        pig.last_fight_date = ""
        pig.last_quest_time = ""
        pig.last_mining_time = ""
        msg = "♻️ Всі позиційні таймери скинуто\n"

    else:
        updated = False
        msg = f"❌ Невідома властивість: {field}\n"

    if updated:
        death_msg = handle_death(pig)
        db.save_pig(pig)
        if death_msg:
            msg += f"\n{death_msg}"

    await message.answer(msg)
