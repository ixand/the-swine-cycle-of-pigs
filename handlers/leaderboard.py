from aiogram import types
from storage import db

async def leaderboard_handler(message: types.Message):
    all_pigs = db.get_all_pigs()

    if not all_pigs:
        await message.answer("Поки що немає жодного хряка у грі!")
        return

    # Сортуємо за XP
    top_pigs = sorted(all_pigs, key=lambda p: (p.level, p.xp), reverse=True)[:10]

    text = "🏆 Топ хряків:\n"
    for idx, pig in enumerate(top_pigs, start=1):
        text += f"{idx}. {pig.name} — рівень {pig.level}, досвід {pig.xp}\n"

    await message.answer(text)
