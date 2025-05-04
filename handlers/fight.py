from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from storage import db
from services.pig_service import fight
from services.pig_service import check_level_up, get_rank
import random

# Тимчасова пам'ять активних спарингів
pending_sparrings = {}

async def sparring_request_handler(message: types.Message):
    user_id = message.from_user.id
    pig = db.get_pig(user_id)

    if not pig:
        await message.answer("Ти ще не маєш хряка! Використай /start")
        return
    
    # Створюємо кнопку для прийняття виклику
    builder = InlineKeyboardBuilder()
    builder.button(text="Прийняти виклик 🐖", callback_data=f"accept_sparring:{user_id}")

    pending_sparrings[user_id] = True  # Запам'ятовуємо, що виклик активний

    await message.answer(
        f"🐷 {pig.name} викликає на спаринг!\nНатисни кнопку, щоб прийняти виклик!",
        reply_markup=builder.as_markup()
    )

async def sparring_accept_handler(callback: types.CallbackQuery):
    data = callback.data
    if not data.startswith("accept_sparring:"):
        return

    opponent_id = int(data.split(":")[1])
    challenger_id = callback.from_user.id

    if opponent_id == challenger_id:
        await callback.answer("Не можна приймати свій власний виклик!")
        return

    if opponent_id not in pending_sparrings:
        await callback.answer("Цей виклик уже не активний або був прийнятий.")
        return

    pig1 = db.get_pig(opponent_id)
    pig2 = db.get_pig(challenger_id)

    if not pig1 or not pig2:
        await callback.message.answer("Один з учасників не має хряка!")
        return

    # Перевіряємо здоров'я
    if pig1.health < 13:
        await callback.answer("У тебе недостатньо здоров'я для спарингу! Потрібно мінімум 13 ❤️.", show_alert=True)
        return
    
    if pig2.health < 13:
        await callback.answer("У тебе недостатньо здоров'я для спарингу! Потрібно мінімум 13 ❤️.", show_alert=True)
        return

    # Видаляємо активний виклик і кнопку
    del pending_sparrings[opponent_id]

    await callback.message.edit_reply_markup(reply_markup=None)  # Видаляємо кнопку

    # Бій
    winner, loser, xp_transfer = fight(pig1, pig2)



    db.save_pig(pig1)
    db.save_pig(pig2)

    text = (
        f"⚔️ Спаринг між {pig1.name} та {pig2.name} завершено!\n"
        f"🏆 Переможець: {winner.name}\n"
        f"➕ Переможець отримує {xp_transfer} XP.\n"
        f"➖ Переможений втрачає {xp_transfer} XP."
    )

    level_ups = check_level_up(winner)
    if level_ups > 0:
        text += f"\n🏅 Твій хряк підняв рівень на {level_ups}!\n➕ Сила +{level_ups}, Здоров'я +{level_ups * 10}\n"
     # Перевірка на новий ранг
    if winner.level in (5, 10, 20):
        new_rank = get_rank(winner)
        text += f"🎖️ Вітаємо! Твій хряк досяг рангу: {new_rank}!"
    await callback.message.answer(text)
    await callback.answer()
