from aiogram import types
from storage import db
from services.pig_service import feed_pig, get_allowed_feedings
from datetime import datetime
from utils.constants import FEED_COOLDOWN_MINUTES
from utils.pig_helpers import ensure_pig_exists

async def feed_handler(message: types.Message):
    user_id = message.from_user.id
    pig = await ensure_pig_exists(message, user_id)
    if not pig:
        return

    now = datetime.now()
    if not pig.last_feed_time or now.strftime("%Y-%m-%d") != pig.last_feed_time[:10]:
        pig.feeds_today = 0

    allowed_feedings = get_allowed_feedings(pig)

    if pig.feeds_today >= allowed_feedings:
        await message.answer(f"Сьогодні твого хряка вже годували {pig.feeds_today} раз(и). Більше годувати не можна!")
        return

    if pig.last_feed_time:
        last_feed_dt = datetime.fromisoformat(pig.last_feed_time)
        elapsed = (now - last_feed_dt).total_seconds()
        cooldown_seconds = FEED_COOLDOWN_MINUTES * 60

        if elapsed < cooldown_seconds:
            minutes_left = int((cooldown_seconds - elapsed) // 60) + 1
            await message.answer(f"Ще рано годувати! Спробуй через {minutes_left} хвилин(и).")
            return

    pig.feeds_today += 1
    pig.last_feed_time = now.isoformat()
    level_ups, rank_msg = feed_pig(pig)
    db.save_pig(pig)

    text = (
        f"Твій хряк погодований!\n"
        f"Нова вага: {pig.weight} кг\n"
        f"Досвід: {pig.xp}\n"
        f"Сила: {pig.strength}\n"
        f"Розум: {pig.mind}\n"
        f"Годувань сьогодні: {pig.feeds_today}/{allowed_feedings}"
    )
    if rank_msg:
        text += f"\n{rank_msg}"

    await message.answer(text)
