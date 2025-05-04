from aiogram import types
from storage import db
from services.pig_service import feed_pig, get_allowed_feedings
from datetime import datetime, timedelta

async def feed_handler(message: types.Message):
    user_id = message.from_user.id
    pig = db.get_pig(user_id)

    if not pig:
        await message.answer("Ти ще не маєш хряка! Використай /start")
        return

    now = datetime.now()

    # Якщо новий день — обнуляємо кількість годувань
    if not pig.last_feed_time or now.strftime("%Y-%m-%d") != pig.last_feed_time[:10]:
        pig.feeds_today = 0

    allowed_feedings = get_allowed_feedings(pig)

    # Перевіряємо кількість годувань на день
    if pig.feeds_today >= allowed_feedings:
        await message.answer(f"Сьогодні твого хряка вже годували {pig.feeds_today} раз(и). Більше годувати не можна!")
        return

       # Перевіряємо проміжок між годуваннями (мінімум 3 хвилини для тестів)
    if pig.last_feed_time:
        last_feed_dt = datetime.fromisoformat(pig.last_feed_time)
        elapsed = (now - last_feed_dt).total_seconds()

        cooldown_seconds = 0.1 * 60  # 60 хвилин

        if elapsed < cooldown_seconds:
            minutes_left = int((cooldown_seconds - elapsed) // 60) + 1  # округлюємо вгору
            await message.answer(f"Ще рано годувати! Спробуй через {minutes_left} хвилин(и).")
            return


    # Якщо все ок — годуємо
    feed_pig(pig)
    pig.feeds_today += 1
    pig.last_feed_time = now.isoformat()
    db.save_pig(pig)

    await message.answer(
        f"Твій хряк погодований!\nНова вага: {pig.weight} кг\nДосвід {pig.xp}\nСила: {pig.strength}\nГодувань сьогодні: {pig.feeds_today}/{allowed_feedings}"
    )
