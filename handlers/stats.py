from aiogram import types
from storage import db
from services.pig_service import get_rank

async def stats_handler(message: types.Message):
    if message.reply_to_message:
        target_user = message.reply_to_message.from_user
        user_id = target_user.id
        is_self = user_id == message.from_user.id
    else:
        user_id = message.from_user.id
        is_self = True

    pig = db.get_pig(user_id)

    if not pig:
        if is_self:
            await message.answer("Ти ще не маєш хряка! Використай /start")
        else:
            await message.answer("У цього користувача ще немає хряка 🐷")
        return

    rank = get_rank(pig)

    health = round((pig.health / pig.max_health) * 100,2)

    owner = "Твій хряк" if is_self else f"Хряк {pig.name} користувача @{target_user.username or target_user.first_name}"

    await message.answer(
        f"{owner}:\n"
        f"🏅 Ранг: {rank}\n"
        f"📈 Рівень: {pig.level}\n"
        f"✨ Досвід: {pig.xp} XP\n"
        f"⚔️ Сила: {pig.strength}\n"
        f"🧠 Розум: {pig.mind}\n"
        f"❤️ Здоров'я: {pig.health} - {health}%\n"
        f"🪙 Золото: {pig.gold}\n"
        f"⚖️ Вага: {pig.weight} кг"
    )
