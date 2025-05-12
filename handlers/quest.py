from aiogram import types
from storage import supabase_storage as db
from services.quest_service import apply_quest
from datetime import datetime, timedelta
from utils.constants import QUEST_COOLDOWN_HOURS
from utils.pig_helpers import ensure_pig_exists

async def quest_handler(message: types.Message):
    user_id = message.from_user.id
    pig = await ensure_pig_exists(message, user_id)
    if not pig:
        return

    last_quest_time_str = getattr(pig, "last_quest_time", "")

    if last_quest_time_str:
        try:
            last_quest_time = datetime.strptime(last_quest_time_str, "%Y-%m-%d %H:%M:%S")
            time_diff = datetime.now() - last_quest_time
        except ValueError:
            time_diff = timedelta(hours=999)
    else:
        time_diff = timedelta(hours=999)

    if time_diff < timedelta(hours=QUEST_COOLDOWN_HOURS):
        remaining_time = timedelta(hours=QUEST_COOLDOWN_HOURS) - time_diff
        hours_remaining = remaining_time.seconds // 3600
        minutes_remaining = (remaining_time.seconds % 3600) // 60
        await message.answer(
            f"Ти можеш пройти квест лише через {hours_remaining} годин(и) та {minutes_remaining} хвилин. Спробуй знову пізніше."
        )
        return

    quest, level_ups, rank_msg = apply_quest(pig)
    db.save_pig(pig)

    text = f"🎯 Квест: *{quest['title']}*\n\n{quest['description']}\n\n🎁 Нагорода: " + \
        ", ".join([f"+{v} {k}" for k, v in quest["effects"].items()])

    if rank_msg:
        text += f"\n{rank_msg}"

    await message.answer(text, parse_mode="Markdown")
