import asyncio
import random
from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from storage import db
from services.pig_service import fight, check_level_up, get_rank

# Тимчасова пам'ять активних спарингів
pending_sparrings = {}

async def sparring_request_handler(message: types.Message):
    user_id = message.from_user.id
    pig = db.get_pig(user_id)

    if not pig:
        await message.answer("Ти ще не маєш хряка! Використай /start")
        return

    builder = InlineKeyboardBuilder()
    builder.button(text="Прийняти виклик 🐖", callback_data=f"accept_sparring:{user_id}")

    pending_sparrings[user_id] = True

    await message.answer(
        f"🐷 {pig.name} викликає на спаринг!\nНатисни кнопку, щоб прийняти виклик!",
        reply_markup=builder.as_markup()
    )

async def sparring_accept_handler(callback: types.CallbackQuery):
    await callback.answer()  # Обов'язково одразу, щоб Telegram не викидав помилку

    data = callback.data
    if not data.startswith("accept_sparring:"):
        return

    opponent_id = int(data.split(":")[1])
    challenger_id = callback.from_user.id

    if opponent_id == challenger_id:
        return await callback.message.answer("Не можна приймати свій власний виклик!")

    if opponent_id not in pending_sparrings:
        return await callback.message.answer("Цей виклик уже не активний або був прийнятий.")

    pig1 = db.get_pig(opponent_id)
    pig2 = db.get_pig(challenger_id)

    if not pig1 or not pig2:
        return await callback.message.answer("Один з учасників не має хряка!")

    if pig1.health < 13 or pig2.health < 13:
        return await callback.message.answer("У одного з хряків недостатньо здоров'я для спарингу (мінімум 13 ❤️).")

    del pending_sparrings[opponent_id]
    await callback.message.edit_reply_markup(reply_markup=None)

    # Унікальні сценарії бою з обов'язковими і додатковими етапами
    base_events = [
        f"{pig1.name} різко атакує — класичний початок!",
        f"{pig2.name} ухиляється і робить підсічку!",
        f"Сутичка набирає обертів, гримлять підкови і каплють піт...",
        f"{pig1.name} ледь встигає зреагувати на хитрий маневр суперника!",
        f"{pig2.name} тим часом використовує свою масу на повну!",
        f"Несподівано {pig1.name} видає комбо!",
        f"{pig2.name} на мить завмирає, але знаходить в собі сили продовжити!",
        f"Останній удар... хто ж переможе?!"
    ]

    # Додаємо рандомну кількість подій (мін 5, макс 8)
    fight_script = random.sample(base_events, k=random.randint(5, len(base_events)))

    for line in fight_script:
        await callback.message.answer(line)
        await asyncio.sleep(random.uniform(2.5, 4.5))

    # Фінал бою
    winner, loser, xp_transfer = fight(pig1, pig2)
    db.save_pig(pig1)
    db.save_pig(pig2)

    result_text = (
        f"\n🏁 Спаринг завершено!\n"
        f"🏆 Переможець: <b>{winner.name}</b>\n"
        f"➕ Отримано {xp_transfer} XP\n"
        f"➖ Програв {xp_transfer} XP"
    )

    level_ups = check_level_up(winner)
    if level_ups > 0:
        result_text += f"\n📈 Рівень підвищено на {level_ups}!"
        if winner.level in (5, 10, 20):
            result_text += f"\n🎖️ Новий ранг: {get_rank(winner)}!"

    await callback.message.answer(result_text, parse_mode="HTML")
