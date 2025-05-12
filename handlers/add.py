from aiogram import types
from aiogram.filters import CommandObject
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
    if len(parts) < 1:
        await message.answer("⚠️ Використай: /add [тип] [значення]")
        return

    field = parts[0].lower()
    amount = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 0

    updated = True
    msg = ""

    if field == "xp":
        pig.xp += amount
        msg = f"✨ Додано {amount} XP"
    elif field == "str":
        pig.strength += amount
        msg = f"⚔️ Додано {amount} сили"
    elif field == "min":
        pig.mind += amount
        msg = f"🧠 Додано {amount} розуму"
    elif field == "hp":
        pig.health += amount
        msg = f"❤️ Додано {amount} здоров'я"
    elif field == "mhp":
        pig.max_health += amount
        msg = f"❤️‍🩹 Додано {amount} до максимального здоров'я"
    elif field == "gol":
        pig.gold += amount
        msg = f"🪙 Додано {amount} золота"
    elif field == "mas":
        pig.weight += amount
        msg = f"⚖️ Додано {amount} кг ваги"
    elif field == "pos":
        pig.last_feed_time = ""
        pig.last_fight_date = ""
        pig.last_quest_time = ""
        pig.last_mining_time = ""
        msg = "♻️ Всі позиційні таймери скинуто"
    else:
        updated = False
        msg = f"❌ Невідома властивість: {field}"

    if updated:
        db.save_pig(pig)

    await message.answer(msg)