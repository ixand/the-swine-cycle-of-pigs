from aiogram import types
from storage import db
from services.quest_service import apply_quest
from datetime import datetime, timedelta

async def quest_handler(message: types.Message):
    user_id = message.from_user.id
    pig = db.get_pig(user_id)

    if not pig:
        await message.answer("Ти ще не маєш хряка! Використай /start")
        return

    # Отримуємо час останнього квесту і перевіряємо, чи минуло 4 години
    last_quest_time_str = getattr(pig, "last_quest_time", "")
    
    if last_quest_time_str:
        try:
            last_quest_time = datetime.strptime(last_quest_time_str, "%Y-%m-%d %H:%M:%S")
            time_diff = datetime.now() - last_quest_time
        except ValueError:
            # Якщо дата некоректна, то даємо можливість виконати квест
            time_diff = timedelta(hours=999)
    else:
        time_diff = timedelta(hours=999)  # Якщо квесту ще не було, даємо можливість

    # Перевіряємо, чи пройшло 4 години з останнього квесту
    if time_diff < timedelta(hours=4):
        remaining_time = timedelta(hours=4) - time_diff
        
        # Отримуємо кількість годин і хвилин для залишкового часу
        hours_remaining = remaining_time.seconds // 3600
        minutes_remaining = (remaining_time.seconds % 3600) // 60
        
        # Формуємо повідомлення
        await message.answer(f"Ти можеш пройти квест лише через {hours_remaining} годин(и) та {minutes_remaining} хвилин. Спробуй знову через кілька годин.")
        return

    # Перевіряємо, чи виконано квест сьогодні
    last_quest_date_str = getattr(pig, "last_quest_date", "")
    last_quest_date = datetime.strptime(last_quest_date_str, "%Y-%m-%d") if last_quest_date_str else None
    today = datetime.now().date()

    if last_quest_date and last_quest_date == today:
        await message.answer("Ти вже виконав квест сьогодні. Спробуй завтра!")
        return

    # Виконання квесту
    quest = apply_quest(pig)
    db.save_pig(pig)

    # Оновлюємо дату та час останнього квесту
    pig.last_quest_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Оновлюємо час
    pig.last_quest_date = datetime.now().strftime("%Y-%m-%d")  # Оновлюємо тільки дату
    db.save_pig(pig)

    # Виводимо текст квесту та нагороду
    text = f"🎯 Квест: *{quest['title']}*\n\n{quest['description']}\n\n🎁 Нагорода: " + \
        ", ".join([f"+{v} {k}" for k, v in quest["effects"].items()])
    
    await message.answer(text, parse_mode="Markdown")
