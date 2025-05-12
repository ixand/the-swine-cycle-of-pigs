from aiogram import types
from aiogram.filters import CommandObject
from storage import supabase_storage as db
from utils.pig_helpers import ensure_pig_exists
from services.pig_service import check_level_up

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

    if field == "xp":
        pig.xp += amount
        msg = f"✨ Додано {amount} XP"
    elif field == "lvl":
        pig.level += amount
        msg = f"⬆️ Додано {amount} рівнів"
        level_ups, rank_msg = check_level_up(pig)
        if level_ups:
            msg += f"\n🎉 {rank_msg or 'Хряк отримав бонуси за нові рівні!'}"
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
